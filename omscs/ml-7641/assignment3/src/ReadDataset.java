package edu.gatech.ml.assignment3;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import shared.DataSet;
import shared.DataSetDescription;
import shared.Instance;
import util.linalg.DenseVector;
import util.linalg.Vector;

public class ReadDataset {

	private String filename;

	public ReadDataset(String filename) {
		this.filename = filename;
	}
	
	public DataSet read() {
		BufferedReader br;
		DataSet set = null;
		try {
			br = new BufferedReader(new FileReader(this.filename));
			
	        String line;
	        List<Instance> data = new ArrayList<Instance>();
	        Pattern pattern = Pattern.compile("[ ,]+");
	        while ((line = br.readLine()) != null) {
	            String[] split = pattern.split(line.trim());
	            double[] input = new double[split.length - 1];
	            for (int i = 0; i < input.length; i++) {
	                input[i] = Double.parseDouble(split[i]);
	            }
	            int label = ((int)split[input.length].charAt(0) - (int)'A');
	            double[] labelValues = new double[26];
	            for(int i=0; i<26; i++) {
	            	if(i==label) labelValues[i]=1;
	            	else labelValues[i] = 0;
	            }
	            Instance instance = new Instance((Vector) new DenseVector(input), new Instance(labelValues));
	            data.add(instance);
	        }
	        br.close();
	        Instance[] instances = (Instance[]) data.toArray(new Instance[0]);
	        set = new DataSet(instances);
	        set.setDescription(new DataSetDescription(set));
		} catch (NumberFormatException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return set;
	    	
	}
	
}
