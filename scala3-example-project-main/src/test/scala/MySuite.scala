import scala.concurrent.Await
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.DurationInt
import java.io.ByteArrayOutputStream
import java.io.PrintStream
import scala.util.{Failure, Success}

class MySuite extends munit.FunSuite {

  test("GivenInstances parses Int and Option[Int]") {
    import GivenInstances.StringParser.given

    val intParser = summon[GivenInstances.StringParser[Int]]
    val optIntParser = summon[GivenInstances.StringParser[Option[Int]]]

    assertEquals(intParser.parse("21"), Success(21))
    assertEquals(optIntParser.parse(""), Success(None))
    assertEquals(optIntParser.parse("42"), Success(Some(42)))
    assert(optIntParser.parse("x").isFailure)
  }

  test("ContextFunctions.parse.sumStrings returns sum for valid numbers") {
    import GivenInstances.StringParser.given

    val result = ContextFunctions.parse.sumStrings("3", "4")
    assertEquals(result, Success(7))
  }

  test("ContextFunctions.parse.sumStrings fails for invalid number") {
    import GivenInstances.StringParser.given

    val result = ContextFunctions.parse.sumStrings("3", "a")
    assert(result.isFailure)
  }

  test("ContextFunctions.context async operations compute expected values") {
    val sumF = ContextFunctions.context.asyncSum(3, 4)
    val multF = ContextFunctions.context.asyncMult(3, 4)

    assertEquals(Await.result(sumF, 2.seconds), 7)
    assertEquals(Await.result(multF, 2.seconds), 12)
  }

  test("Conversion.convert and useConversion transform IntWrapper to DoubleWrapper") {
    val converted = Conversion.convert(Conversion.IntWrapper(42))
    val inferred = Conversion.useConversion

    assertEquals(converted, Conversion.DoubleWrapper(42.0))
    assertEquals(inferred, Conversion.DoubleWrapper(4.0))
  }

  test("EnumTypes.Planet computes positive gravity and sensible relative weights") {
    val earthGravity = EnumTypes.Planet.Earth.surfaceGravity
    val mercuryGravity = EnumTypes.Planet.Mercury.surfaceGravity

    assert(earthGravity > 0)
    assert(mercuryGravity > 0)
    assert(earthGravity > mercuryGravity)

    val massFor80kgOnEarth = 80.0 / earthGravity
    val weightOnEarth = EnumTypes.Planet.Earth.surfaceWeight(massFor80kgOnEarth)
    assert(math.abs(weightOnEarth - 80.0) < 1e-9)
  }

  test("EnumTypes.ListEnum can be built and pattern matched") {
    import EnumTypes.ListEnum

    val list = ListEnum.Cons(1, ListEnum.Cons(2, ListEnum.Empty))

    val obtained = list match
      case ListEnum.Cons(h, ListEnum.Cons(h2, ListEnum.Empty)) => h + h2
      case _ => -1

    assertEquals(obtained, 3)
  }

  test("UnionTypes custom list supports head/tail decomposition") {
    val list: UnionTypes.Cons[Int] = UnionTypes.Cons(1, UnionTypes.Cons(2, UnionTypes.Cons(3, UnionTypes.Empty)))

    val obtained = list match
      case UnionTypes.Cons(h, UnionTypes.Cons(h2, _)) => h + h2
      case _ => -1

    assertEquals(obtained, 3)
  }

  test("PatternMatching booleanPattern.Even matches even-length strings") {
    val even = "even" match
      case PatternMatching.booleanPattern.Even() => true
      case _ => false

    val odd = "odd" match
      case PatternMatching.booleanPattern.Even() => true
      case _ => false

    assert(even)
    assert(!odd)
  }

  test("PatternMatching product extractor returns swapped positions by Product implementation") {
    val obtained = ("john", 42) match
      case PatternMatching.productPattern.Person(n, a) => (n, a)

    assertEquals(obtained, (42, "john"))
  }

  test("PatternMatching seq extractor supports full names") {
    val obtained = PatternMatching.seqPattern.Names.unapplySeq("Alan Mathison Turing")

    assertEquals(obtained, Some(scala.List("Turing", "Alan", "Mathison")))
    assertEquals(PatternMatching.seqPattern.Names.unapplySeq("john"), None)
  }

  test("PatternMatching name extractor rejects empty input") {
    val nonEmptyMatched = "alice" match
      case PatternMatching.namePattern.Name(n) => n == "alice"
      case _ => false

    val emptyMatched = "" match
      case PatternMatching.namePattern.Name(_) => true
      case _ => false

    assert(nonEmptyMatched)
    assert(!emptyMatched)
  }

  test("StructuralTypes valid person exposes required fields") {
    assertEquals(StructuralTypes.person.name, "Emma")
    assertEquals(StructuralTypes.person.age, 42)
  }

  test("StructuralTypes invalid person throws when accessing missing age") {
    intercept[NoSuchElementException] {
      StructuralTypes.invalidPerson.age
    }
  }

  test("TypeLambdas aliases can be materialized with expected runtime values") {
    val m: TypeLambdas.M[String, Int] = Map(1 -> "one")
    val tuple: TypeLambdas.Tuple[String] = ("a", "b")

    assertEquals(m.get(1), Some("one"))
    assertEquals(tuple._1, "a")
    assertEquals(tuple._2, "b")
  }

  test("TraitParams classes keep trait constructor message") {
    val a = new TraitParams.A
    val b = new TraitParams.B

    assertEquals(a.msg, "Hello")
    assertEquals(b.msg, "Dotty!")
  }

  test("IntersectionTypes.Point supports x and y and tpe is intentionally not implemented") {
    val p = IntersectionTypes.Point(3, 4)
    assertEquals(p.x, 3.0)
    assertEquals(p.y, 4.0)

    intercept[NotImplementedError] {
      p.tpe
    }
  }

  test("Multiversal equality can be enabled between unrelated local types") {
    import scala.language.strictEquality

    class A(val a: Int)
    class B(val b: Int)

    given CanEqual[A, B] = CanEqual.derived
    given CanEqual[B, A] = CanEqual.derived

    val a = new A(1)
    val b = new B(1)

    assert(a != b)
    assert(!(b == a))
  }

  test("PatternMatching seq extractor trims boundary spaces") {
    val obtained = PatternMatching.seqPattern.Names.unapplySeq("  Alan Turing  ")
    assertEquals(obtained, Some(scala.List("Turing", "Alan")))
  }

  test("PatternMatching boolean extractor treats empty string as even") {
    val obtained = "" match
      case PatternMatching.booleanPattern.Even() => true
      case _ => false

    assert(obtained)
  }

  test("Main runs all example sections") {
    val output = new ByteArrayOutputStream()
    Console.withOut(new PrintStream(output)) {
      Main()
    }

    val text = output.toString("UTF-8")
    val expectedSections = Seq(
      "Trait Params example:",
      "Enum Types example:",
      "Context Functions example:",
      "Given Instances example:",
      "Conversion example:",
      "Union Types example:",
      "Intersection Types example:",
      "Type Lambda example:",
      "Multiversal Equality example:",
      "Parameter Untupling example:",
      "Structural Types example:",
      "Pattern Matching example:"
    )

    expectedSections.foreach(section => assert(text.contains(section)))
  }
}
