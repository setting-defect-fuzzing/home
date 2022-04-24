
import java.util.*;
import java.io.*;

import soot.PackManager;
import soot.SceneTransformer;
import soot.Transform;
import soot.options.Options;
import org.json.JSONArray;
import org.json.JSONObject;

public class TestApp {
	static File analysisFile;
	static String apkname,apkdir,filePathIn;
	static JSONArray patterns;
	
	public static void main(String[] args) throws IOException 
	{
		PrintStream stdout = System.out;
		String path = args[3];		
		File file = new File(path);		
		File[] fs = file.listFiles();	
		for(File f:fs){
			if(!f.isDirectory()){
				System.out.println(f);
				startsoot(args,f.toString());
				System.setOut(stdout);
			}
		}
	}
	public static void startsoot(String[] args, String apkpath) throws IOException{
		soot.G.reset();
		String[] sootlist=handleargs(args,apkpath);
		PrintStream ps = new PrintStream(analysisFile);
		System.setOut(ps);
		Options.v().set_src_prec(Options.src_prec_apk);
		Options.v().set_output_format(Options.output_format_jimple);
		Options.v().set_no_writeout_body_releasing(true);

		PackManager.v().getPack("wjtp").add(new Transform("wjtp.myTrans", new SceneTransformer(){
			@Override
			protected void internalTransform(String arg0, Map<String, String> arg1) {
				Main flowAnalysis = new Main();
				for(int j=0; j < patterns.length(); j++) { // Iterate each element in the elements array
					JSONObject pattern =  patterns.getJSONObject(j);
					System.out.println("#######################################");
					System.out.println("Name:"+pattern.getString("name"));
					flowAnalysis.findbug(apkname,pattern);
					System.out.println();
				}
			}
		}));
		
		soot.Main.main(sootlist);
	}
	/**
	 * 解析输入
	 * @param args
	 * @throws IOException
	 */
	public static String[] handleargs(String[] args,String apkpath) throws IOException{
		String[] sootlist = args;
		sootlist[3]=apkpath;
		String[] list = sootlist[3].split("\\\\");
		apkname = list[list.length-1].substring(0,list[list.length-1].length()-4);
		analysisFile = new File("../output/sootOutput/"+apkname+"\\allmappings.txt");
		apkdir = "../output/sootOutput/"+apkname;
		File file=new File("../output/sootOutput/");
		if(!file.exists()){
			file.mkdir();}
		sootlist[1] = apkdir;
		String JsonContext = new Util().ReadFile("resource/allmappings.json");
		JSONObject rootObject = new JSONObject(JsonContext); // Parse the JSON to a JSONObject
		patterns = rootObject.getJSONArray("pattern");
		file=new File(apkdir);
		if(!file.exists()){
			file.mkdir();}
		return sootlist;
	}

	public void addpattern(String path) throws IOException
	{
		FileInputStream fileInputStream = new FileInputStream(path);
		InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream, "UTF-8");
		BufferedReader reader = new BufferedReader(inputStreamReader);
		String tempString = null;
		JSONObject pattern =new JSONObject();
		JSONArray mainapis=new JSONArray();
		JSONArray controlcheckbefores=new JSONArray();
		while((tempString = reader.readLine()) != null){
			if(tempString.startsWith("Permission:")) 
			{
				if(mainapis.length()>0)
				{
					pattern.put("mainapi", mainapis);
					patterns.put(pattern);
				}
				mainapis.clear();
				controlcheckbefores.clear();
				pattern.clear();
				String permission = tempString.substring(tempString.indexOf("Permission:"),tempString.length()-1);
				JSONObject controlcheckbefore=new JSONObject();
				controlcheckbefore.put("methodname",permission);
				controlcheckbefores.put(controlcheckbefore);
				pattern.put("controlcheckbefore", controlcheckbefores);
			}
			else{
				if (tempString.startsWith("<")) 
				{
					String classname = tempString.substring(1,tempString.indexOf(':'));
					String methodname = tempString.substring(1,tempString.indexOf('('));
					methodname = methodname.substring(methodname.lastIndexOf(' '),methodname.length());
					JSONObject mainapi=new JSONObject();
					mainapi.put("methodname",methodname);
					mainapi.put("classname",classname);
					mainapis.put(mainapi);
				}
			}
		}
		reader.close();
	}
	
}