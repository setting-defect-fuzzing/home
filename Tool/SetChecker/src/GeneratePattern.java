
import java.io.*;
import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;


public class GeneratePattern {
    
    public static void main(String[] args) throws IOException 
	{
        String path="resource/allmappings";
        String writepath="resource/allmappings.json";
		FileInputStream fileInputStream = new FileInputStream("resource/dangerouslist.txt");
		InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream, "UTF-8");
		BufferedReader reader = new BufferedReader(inputStreamReader);
		String dangerouString = "";
		ArrayList<String> dangerouList = new ArrayList<String>();
		while((dangerouString=reader.readLine()) != null){
			dangerouList.add(dangerouString);
		}
		reader.close();
        addpattern(path,writepath,dangerouList);
    }
    public static void addpattern(String path,String writepath,ArrayList<String> dangerouList) throws IOException
	{
        JSONArray patterns = new JSONArray();
		FileInputStream fileInputStream = new FileInputStream(path);
		InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream, "UTF-8");
		BufferedReader reader = new BufferedReader(inputStreamReader);
		String tempString = null;
		JSONObject pattern =new JSONObject();
		JSONArray mainapis=new JSONArray();
		JSONArray controlcheckbefores=new JSONArray();
		boolean flag = false;
		while((tempString = reader.readLine()) != null){
			if(tempString.startsWith("Permission:")) 
			{
				flag = false;
				for (String dangerouString : dangerouList) {
					if(tempString.contains(dangerouString)){
						flag = true;
						break;
					}
				}
				if(flag==true){
					if(mainapis.length()>0)
					{
						pattern.put("mainapi", mainapis);
						JSONArray controlcheckafter=new JSONArray();
						JSONArray flowgen=new JSONArray();
						JSONArray flowkill=new JSONArray();
						JSONArray flowfind=new JSONArray();
						pattern.put("controlcheckafter", controlcheckafter);
						pattern.put("flowgen", flowgen);
						pattern.put("flowkill", flowkill);
						pattern.put("flowfind", flowfind);
						patterns.put(pattern);
					}
					mainapis=new JSONArray();
					controlcheckbefores=new JSONArray();
					pattern =new JSONObject();
					String permission = tempString.substring(tempString.indexOf("Permission:")+11,tempString.length());
					JSONObject controlcheckbefore=new JSONObject();
					controlcheckbefore.put("methodname",permission);
					controlcheckbefore.put("classname","");
					controlcheckbefores.put(controlcheckbefore);
					pattern.put("controlcheckbefore", controlcheckbefores);
					pattern.put("name", permission);
				}
			}
			else{
				if(flag==true){
					if (tempString.startsWith("<")) 
					{
						String classname = tempString.substring(1,tempString.indexOf(':'));
						String methodname = tempString.substring(1,tempString.indexOf('('));
						methodname = methodname.substring(methodname.lastIndexOf(' ')+1,methodname.length());
						JSONObject mainapi=new JSONObject();
						mainapi.put("methodname",methodname);
						mainapi.put("classname",classname);
						mainapis.put(mainapi);
					}
					if (tempString.startsWith("End"))
					{
						System.out.println();
					}
				}
			}
		}
        JSONObject all_pattern =new JSONObject();
        all_pattern.put("pattern",patterns);
		reader.close();
        FileWriter fw = new FileWriter(writepath);
        PrintWriter out = new PrintWriter(fw);
        out.write(all_pattern.toString());
        out.println();
        fw.close();
        out.close();
    }
}