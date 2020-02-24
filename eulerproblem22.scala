import scala.io.Source

val fileContents = Source.fromFile("/home/karl/Downloads/p022_names.txt").getLines.mkString.trim
val L = fileContents.split(',').toList.sorted
val charMap = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".toList zip (1 to 26)).toMap
val nameList = L zip (1 to L.size)
val ans = nameList.map(x => (x._1.map(x => charMap.getOrElse(x,0)).sum*x._2)).sum
println(ans)

