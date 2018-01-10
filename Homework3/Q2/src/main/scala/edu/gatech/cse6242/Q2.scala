package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {

	def main(args: Array[String]) {
    	val sc = new SparkContext(new SparkConf().setAppName("Q2"))
		val sqlContext = new SQLContext(sc)
		import sqlContext.implicits._

    	// read the file
    	val file = sc.textFile("hdfs://localhost:8020" + args(0))

		/* TODO: Needs to be implemented */
		var source = file.map(_.split("\t")).map(token => (token(0),(-1)*token(2).toInt)).filter(_._2 <= -5).toDF("source", "outweight")
		var target = file.map(_.split("\t")).map(token => (token(1),token(2).toInt)).filter(_._2 >= 5).toDF("target", "inweight")
		var total = source.unionAll(target).withColumnRenamed("node", "weight")
		var result = total.groupBy("source").agg(sum("outweight"))
		result.show()
		var output = result.map(token => token.mkString("\t"))

    	// store output on given HDFS path.
    	// YOU NEED TO CHANGE THIS
    	output.saveAsTextFile("hdfs://localhost:8020" + args(1))
  	}
}
