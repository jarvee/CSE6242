package edu.gatech.cse6242;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {
    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>{

      private final static IntWritable weight = new IntWritable(1);
      private Text source = new Text();
      private Text target = new Text();

      // learning from the sample in the pdf given by spec
      public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      	// get the single line
        String getLine = value.toString();
        //put the single splitted line into a array
        String[] itr = getLine.split("\t");
        source.set(itr[0]);
        target.set(itr[1]);
        weight.set(Integer.parseInt(itr[2]));
        context.write(target, weight);
      }
    }
    
    public static class IntSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
      private IntWritable result = new IntWritable();

      public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int min = 9999;
        for (IntWritable val : values) {
          if (val.get() < min) {
            min = val.get();
          }
        }
        result.set(min);
        context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
      Configuration conf = new Configuration();
      Job job = Job.getInstance(conf, "Q1");

      /* TODO: Needs to be implemented */
      job.setJarByClass(Q1.class);
      job.setMapperClass(TokenizerMapper.class);
      job.setCombinerClass(IntSumReducer.class);
      job.setReducerClass(IntSumReducer.class);
      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(IntWritable.class);


      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));
      System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}