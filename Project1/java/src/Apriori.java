import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;


public class Apriori {

	
	public boolean is_frequent(String s) {
		return true;
	}
	
	public List find_frequent_1_itemset(){
		return null;
	}
	
	public static void main(String[] args) {

		FileInputStream f = null;
		try {
			f = new FileInputStream("/home/tianyou/courses/CSC240/Adult_Data");
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	    BufferedReader br = new BufferedReader(new InputStreamReader(f));
	    String strline;
	    StringBuffer sb = new StringBuffer();
	    String[] data = null;
	    try {
			while ((strline = br.readLine()) != null)
			{
			    data = strline.split(",");;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	    System.out.println("Data: "+ data);
	}

}
