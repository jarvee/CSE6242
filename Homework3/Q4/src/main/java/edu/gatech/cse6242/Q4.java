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


public class Q4 {
    
    public static class diffMapper extends Mapper<Object, Text, Text, IntWritable>{
        private final static IntWritable out = new IntWritable(1);
        private final static IntWritable in = new IntWritable(-1);
        private Text source = new Text();
        private Text target = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        	String getLine = value.toString();
            String[] itr = getLine.split("\t");
            if (itr.length == 2){
                source.set(itr[0]);
                context.write(source, out);
                target.set(itr[1]);
                context.write(target, in);
            }
        }
    }
    
    public static class diffReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable output = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            output.set(sum);
            context.write(key, output);
        }
    }

    public static class countMapper extends Mapper<Object, Text, Text, IntWritable>{
        private final static IntWritable freq = new IntWritable(1);
        private Text diff = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String getLine = value.toString();
            String[] token = getLine.split("\t");
            diff.set(token[1]);
            context.write(diff, freq);
        }
    }
    
    public static class countReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int total = 0;
            for (IntWritable val : values) {
                total += val.get();
            }
            result.set(total);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job1 = Job.getInstance(conf, "Q4a");

        /* TODO: Needs to be implemented */
        job1.setJarByClass(Q4.class);
        job1.setMapperClass(diffMapper.class);
        job1.setCombinerClass(diffReducer.class);
        job1.setReducerClass(diffReducer.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job1, new Path(args[0]));
        FileOutputFormat.setOutputPath(job1, new Path("procedure"));
        job1.waitForCompletion(true);

        Job job2 = Job.getInstance(conf, "Q4b");
        /* TODO: Needs to be implemented */
        job2.setJarByClass(Q4.class);
        job2.setMapperClass(countMapper.class);
        job2.setCombinerClass(countReducer.class);
        job2.setReducerClass(countReducer.class);
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job2, new Path("procedure"));
        FileOutputFormat.setOutputPath(job2, new Path(args[1]));
        System.exit(job2.waitForCompletion(true) ? 0 : 1);

    }
}