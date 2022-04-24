import java.util.*;
import java.io.File;

import soot.Body;
import soot.Scene;
import soot.SootClass;
import soot.Unit;
import soot.toolkits.graph.*;
import soot.jimple.*;
import soot.Value;
import soot.SootMethod;
import soot.util.Chain;
import soot.jimple.JimpleBody;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Targets;
import soot.toolkits.graph.TrapUnitGraph;
import soot.ValueBox;
import soot.Local;
import soot.MethodOrMethodContext;

import org.json.JSONArray;
import org.json.JSONObject;

public class Main {
    static List<List<Unit>> targetpath = new ArrayList<>();
	static File analysisFile;
	static String apkname,apkdir;
	static List<List<SootMethod>> allpathtospecial = new ArrayList<>();
	static List<SootMethod> firstaddmethod = new ArrayList<>(); //速度优化，反向追溯时，对多个路径经过同一个函数只对第一次经过该函数的前置路径分析
	static JSONObject pattern;
	static List<SootMethod> afterbug = new ArrayList<>();
    
    public void findbug(String name, JSONObject p){
		targetpath.clear();
		allpathtospecial.clear();
		firstaddmethod.clear();
		pattern = p;
        apkname = name;
		Set<SootMethod> specialmethods;
		JSONArray mainapis = pattern.getJSONArray("mainapi");
		JSONArray controlcheckafters = pattern.getJSONArray("controlcheckafter");
		JSONArray controlcheckbefores = pattern.getJSONArray("controlcheckbefore");
		JSONArray flowgens = pattern.getJSONArray("flowgen");
		JSONArray flowfinds = pattern.getJSONArray("flowfind");
		List<SootMethod> warningmethod=new ArrayList<>();
		if (controlcheckbefores.length() >0)
		{
			specialmethods = getSpecialMethods(mainapis);
			for (SootMethod sootMethod :specialmethods){
				List<SootMethod> path = new ArrayList<>();
				path.add(sootMethod);
				findMCallerPath(sootMethod,path);}
			for (List<SootMethod> path : allpathtospecial){
				boolean flag = true;
				if(path.size()>1){
					flag = analysis(path);
				}
				if(flag == false && path.size()>1 && !warningmethod.contains(path.get(1))){
					if (flowgens.length()<1){
						System.out.println("bug:"+path);
					}else{
						System.out.println("warning:"+path);}
					warningmethod.add(path.get(1));}
				if(flag == true && path.size()>1){
					System.out.println("pass:"+path);}}
		}
		if (controlcheckafters.length()>0)
		{
			CallGraph cg = Scene.v().getCallGraph();
			Chain<SootClass> chain = Scene.v().getApplicationClasses();
			for (SootClass sootClass : chain) {
				for (SootMethod method : sootClass.getMethods()) {
					if (method.toString().contains(apkname)){
						try{
							JimpleBody body = (JimpleBody)method.retrieveActiveBody();
							for(int i=0; i < mainapis.length(); i++) {
								if (body.toString().contains(mainapis.getJSONObject(i).getString("methodname"))
								&& body.toString().contains(mainapis.getJSONObject(i).getString("classname"))){
									List<SootMethod> path = new ArrayList<>();
									path.add(method);
									findaftercheck(method,cg,path,controlcheckafters);}}
						}catch (Exception e) {}
						}}}}
		if (flowfinds.length()>0)
		{
			if (mainapis.length()>0){
				for (SootMethod method : warningmethod){
					findnullexception(method,new PatternFlowSet(),pattern);}}
			else{
				Chain<SootClass> chain = Scene.v().getApplicationClasses();
                for (SootClass sootClass : chain) {
                    for (SootMethod method : sootClass.getMethods()) {
						for(int i=0; i < flowgens.length(); i++) {
							if (method.toString().contains(apkname) 
							&& !method.toString().contains(flowgens.getJSONObject(i).getString("methodname"))
							&& !method.toString().contains(flowgens.getJSONObject(i).getString("classname"))){
								try{
									JimpleBody body = (JimpleBody) method.retrieveActiveBody();
									if (body.toString().contains(flowgens.getJSONObject(i).getString("methodname"))
									&& body.toString().contains(flowgens.getJSONObject(i).getString("classname"))){
										findnullexception(method,new PatternFlowSet(),pattern);
									}
								}catch (Exception e) {}
							}}}}}
			
		}
	}
	public static void findaftercheck(SootMethod method,CallGraph cg,List<SootMethod> path,JSONArray controlcheckafters)
	{
		List<SootMethod> thispath = new ArrayList<>();
		if (method.toString().contains(apkname)){
			try{
				JimpleBody body = (JimpleBody)method.retrieveActiveBody();
				for(int i=0; i < controlcheckafters.length(); i++) {
					if (body.toString().contains(controlcheckafters.getJSONObject(i).getString("methodname"))
					&& body.toString().contains(controlcheckafters.getJSONObject(i).getString("classname"))){
						System.out.print("pass:");
						for(SootMethod me:path){
							System.out.print(me+"->");
						}
						System.out.println("end");
						return;
					}
				}
				Iterator<MethodOrMethodContext> targets = new Targets(cg.edgesOutOf(method));
				if (!targets.hasNext() && !afterbug.contains(path.get(0)))
				{
					afterbug.add(path.get(0));
					System.out.print("bug:");
					for(SootMethod me:path){
						System.out.print(me+"->");
					}
					System.out.println("end");
					return;
				}
				thispath.clear();
				while(targets.hasNext()){
					SootMethod tgt = (SootMethod) targets.next();
					// System.out.println(method+" may call "+tgt);
					if(!path.contains(tgt) && method.toString().contains(apkname))
					{
						thispath.addAll(path);
						thispath.add(tgt);
						findaftercheck(tgt,cg,thispath,controlcheckafters);
						thispath.clear();
					}
					
				}

			}catch (Exception e) {}
			
		}
		
	}
	
	/**
	 * 输入一个函数，找到该函数是否使用通过设置获取的变量后没有检查是否为非空就调用 
	 * @param method
	 * @param parameterset
	 */
	public static void findnullexception(SootMethod method,PatternFlowSet parameterset, JSONObject pattern)
    {
		JSONArray flowgens = pattern.getJSONArray("flowgen");
		JSONArray flowkills = pattern.getJSONArray("flowkill");
		JSONArray flowfinds = pattern.getJSONArray("flowfind");
        if (method.toString().contains(apkname) || parameterset.size()>0)
		{
			if(parameterset.size()==0){
				System.out.println("Start==================================================================");
				System.out.println(method.toString());
				if (method.toString().contains("setDataSource")){
					System.out.println(method.toString());
				}
			}
			boolean findnull = false;
			JimpleBody body = new JimpleBody();
			try{
				body = (JimpleBody) method.retrieveActiveBody();
			}catch (Exception e) {
				System.out.println("Exception,findnullexception,retrieveActiveBody");
				return;
			}
            TrapUnitGraph g = new TrapUnitGraph(body);
            PatternFlowSet newset = findassign(body, parameterset);
			try{
				FlowAnalysis npa = new FlowAnalysis(g,newset,flowgens,flowkills);
			}catch (Exception e) {
				return;
			}
            FlowAnalysis npa = new FlowAnalysis(g,newset,flowgens,flowkills);
            for(Unit unit :body.getUnits()){
                Stmt stmt = (Stmt)unit;
                PatternFlowSet setbe = npa.getFlowBefore(unit);
                PatternFlowSet setaf = npa.getFlowAfter(unit);
                if(npa.getFlowBefore(unit).size()>0 || npa.getFlowAfter(unit).size()>0){
                    System.out.println("----------------");
                    System.out.println("method:"+method.toString());
                    System.out.println(unit.toString() + "[in]" +npa.getFlowBefore(unit));
                    System.out.println(unit.toString() + "[out]" +npa.getFlowAfter(unit));}
                if(stmt.containsInvokeExpr() && setbe.size() > 0 ){
                    List<ValueBox> useboxs = stmt.getUseBoxes();
					PatternFlowSet init = new PatternFlowSet();
					SootMethod inme = stmt.getInvokeExpr().getMethod();
					boolean analysisiflag = false;
                    for (ValueBox use : useboxs){
                        if (use.toString().contains("ImmediateBox") && setbe.contains(use.getValue())){
                            init.add(use.getValue());
							analysisiflag = true;}}
					if (analysisiflag == true){
						findnullexception(inme,init,pattern);}}
				for(int i=0; i < flowfinds.length(); i++) {
					if (stmt.toString().contains(flowfinds.getJSONObject(i).getString("methodname")) 
					&& stmt.toString().contains(flowfinds.getJSONObject(i).getString("classname"))){
						List<ValueBox> useboxs = stmt.getUseBoxes();
						if (useboxs.size() >0){
							for (ValueBox use : useboxs){
								if (setbe.contains(use.getValue())){
									System.out.println("**********************Bug**********************");
									System.out.println("firstfindnull:"+stmt.toString());
									System.out.println("value:"+use.getValue().toString());
									System.out.println("method:"+method.toString());
									System.out.println("**********************Bug**********************");
									findnull = true;
									break;}}}
						if (findnull == true){
							break;}}}}
				if(parameterset.size()==0){
					System.out.println("End");
					System.out.println();}
		}

    }
	/**
	 * 在函数中查找参数列表对应的变量，作为数据流分析的初始
	 * @param body
	 * @param initset
	 * @return
	 */
    public static PatternFlowSet findassign(JimpleBody body, PatternFlowSet initset){
        PatternFlowSet newset = new PatternFlowSet();
        if (initset.size()>0){
            List<Local> locals= body.getParameterLocals();
            for(Local local :locals){
                // System.out.println("local:"+local.toString());
                // System.out.println("localtype:"+local.getType().toString());
                for (Value init:initset){
                    if (init.getType().equals(local.getType())){
                        // System.out.println("inittype:"+init.getType().toString());
                        newset.add(local);}}}}
        return newset;
    }
	
	/**
	 * 查找所有最终会调用specialmethod的方法调用路径
	 * @param specialmethod
	 * @param path
	 */
	public static void findMCallerPath(SootMethod specialmethod, List<SootMethod> path) {
		JSONArray mainapis = pattern.getJSONArray("mainapi");
		Set<SootMethod> methods;
		methods = getMethods();
        // System.out.println("Analysis the method [" + specialmethod.toString() + "] ");
		List<SootMethod> callmethods = new ArrayList<>();
        for(SootMethod m : methods){
            if(m.toString().contains(apkname)){
				try{
					Body body = m.retrieveActiveBody();
					for(Unit unit :body.getUnits()){
						Stmt stmt = (Stmt)unit;
						if(stmt.containsInvokeExpr()){
							if(specialmethod != null){
								if (stmt.getInvokeExpr().getMethod().getName().equals(specialmethod.getName()) 
								&& stmt.toString().contains(specialmethod.getDeclaringClass().toString())
								&& !callmethods.contains(m) && !path.contains(m) && !firstaddmethod.contains(m)){ //优化，!path.contains(m)使得到环时停下
									// System.out.println("add:"+m);
									firstaddmethod.add(m);
									callmethods.add(m);
								}
							}
						}
					}
				}catch (Exception e) {

				}
			}
		}
		List<SootMethod> path_copy = new ArrayList<>();
		path_copy.addAll(path);
		if(callmethods.size() > 0){
			for(SootMethod callmethod : callmethods){
				path_copy.add(callmethod);
				findMCallerPath(callmethod,path_copy);
				path_copy.clear();
				path_copy.addAll(path);}}
		else{
			// analysis(path);
			allpathtospecial.add(path_copy);}
	}
	/**
	 * 分析一条方法调用路径上，每个方法的控制流图中是否有对设置进行检查的语句，例如A->B->C，
	 * 则C是使用设置的api，检查在B的控制流图中，包含调用C的语句的路径中，从路径起始到调用C之间是否检查过设置，
	 * 然后再检查在A的控制流图中，包含调用B的语句的路径中，从路径起始到调用B之间是否检查过设置，
	 * 如果都没有，则视为找到一个可能的BUG的其中一个条件被满足。
	 * @param path
	 */
	public static Boolean analysis(List<SootMethod> path){
		// System.out.println("Start");
		// for (SootMethod me : path){
			// System.out.print(me.toString()+"->");}
		// System.out.println();
		SootMethod caller = path.get(0);
		boolean pathflag= false;
		for(int i=1;i<path.size();i++){
			SootMethod target = caller;
			caller = path.get(i);
			boolean checkflag= analysischeckbetween(caller,target);
			if (checkflag == true){
				pathflag = true;}}
		// System.out.println("Right check:"+pathflag);
		// System.out.println("End");
		// System.out.println();
		return pathflag;
	}
	private static boolean analysischeckbetween(SootMethod caller, SootMethod target)
	{
		// System.out.println("**target**"+target);
		// System.out.println("**caller**"+caller);
		JimpleBody body = (JimpleBody)caller.retrieveActiveBody();
		UnitGraph unitGraph = new TrapUnitGraph(body);
		List<Unit> heads = unitGraph.getHeads();
		for (Unit now : heads){
			List<Unit> path = new ArrayList<>();
			path.add(now);
			Unit returnunit = forwardfindtarget(now,unitGraph,target,path);
			List<Unit> path2 = new ArrayList<>();
			path2.add(returnunit);
			getallpath(returnunit,unitGraph,path2);}
		boolean flag = checktargetpath(targetpath);
		if(flag==true){
			System.out.println("find beforecheck:"+caller.toString());
		}
		targetpath = new ArrayList<>();
		// System.out.println("");
		return flag;
	}
	/**
	 * 检查控制流路径中，从起始点到调用函数之间是否检查过设置，返回true（检查过）或false（没有检查过）
	 * @param targetpath
	 * @return
	 */
	private static boolean checktargetpath(List<List<Unit>> targetpath)
	{
		boolean flag = false;
		for(List<Unit> path2 : targetpath){
			// System.out.println("===========");
			for (Unit unit:path2){
				// System.out.println(unit+"->");
				Boolean returncheck = havecheck(unit);
				if(returncheck == true){
					flag = true;}}
			// System.out.println("end");
		}
		return flag;
	}
	/**
	 * 在函数的控制流图unitGraph中倒序查找所有到达目标点now的路径，并将找到的路径存入全局列表targetpath中
	 * @param now
	 * @param unitGraph
	 * @param path2
	 */
	private static void getallpath(Unit now, UnitGraph unitGraph, List<Unit> path2){
		List<Unit> unitlist = unitGraph.getPredsOf(now);
		
		if(unitlist.size()>0){
			for (Unit unit:unitlist){
				if(!path2.contains(unit)){
					path2.add(unit);
					getallpath(unit,unitGraph,path2);}}}
		else{
			targetpath.add(path2);}
	}
	/**
	 * 检查一个语句是否是需要的设置检查语句，可根据pattern进行更改
	 * @param unit
	 * @return
	 */
	private static boolean havecheck(Unit unit){
		JSONArray controlcheckbefores = pattern.getJSONArray("controlcheckbefore");
		for(int i=0; i < controlcheckbefores.length(); i++) {
			JSONObject controlcheckbefore =  controlcheckbefores.getJSONObject(i);
			if (unit!= null && (unit.toString().contains(controlcheckbefore.getString("methodname")) 
			&& unit.toString().contains(controlcheckbefore.getString("classname")))){
				return true;}
		}
		return false;
	}
	/**
	 * 从函数的控制流图中的起始点now开始正序查找目标函数（被调用函数），
	 * 这一步的主要目的是快速找到目标函数在soot中的数据结构，之后便于使用soot方法调用，之前只知道目标函数的名字
	 * @param now
	 * @param unitGraph
	 * @param target
	 * @param path
	 * @return
	 */
	private static Unit forwardfindtarget(Unit now, UnitGraph unitGraph, SootMethod target, List<Unit> path){
		List<Unit> unitlist = unitGraph.getSuccsOf(now);
		Unit returnunit = null;
		if (unitlist.size()>0){
			for (Unit unit:unitlist){
				if(unit.toString().contains(target.getName())){
					// System.out.println("**get it**"+unit.toString());
					return unit;}
				else{
					if (!path.contains(unit)){
						// System.out.println(unit.toString());
						path.add(unit);
						Unit getunit = forwardfindtarget(unit,unitGraph,target,path);
						if (getunit!=null){
							returnunit = getunit;}}}}}
		return returnunit;
	}
	/**
	 * 输入应用的所有类列表，返回所有包含某个字段的函数列表
	 * @param classes
	 * @param methodName
	 * @param className
	 * @return
	 */
	private static Set<SootMethod> getSpecialMethods(JSONArray mainapis)
	{
		Set<SootMethod> methods = new HashSet<SootMethod>();
		Set<SootMethod> mlist = getMethods();
		for (SootMethod method: mlist){
			for(int j=0; j < mainapis.length(); j++) {
				JSONObject mainapi =  mainapis.getJSONObject(j);
				if(method.getName().contains(mainapi.getString("methodname")) 
				&& method.getDeclaringClass().toString().contains(mainapi.getString("classname"))){
					System.out.println("ORIGIN:"+method.toString());
					methods.add(method);}
				if (method.toString().contains(apkname)){
					try{
						JimpleBody body = (JimpleBody)method.retrieveActiveBody();
						for(Unit unit :body.getUnits()){
							Stmt stmt = (Stmt)unit;
							if (stmt.containsInvokeExpr() && stmt.getInvokeExpr().toString().contains(mainapi.getString("methodname")) 
							&& stmt.getInvokeExpr().toString().contains(mainapi.getString("classname"))
							&& !methods.contains(stmt.getInvokeExpr().getMethod())){
								System.out.println("ORIGIN:"+stmt.getInvokeExpr().getMethod().toString());
								methods.add(stmt.getInvokeExpr().getMethod());}}
					}catch (Exception e) {}
				}
			}		
		}
		return methods;
	}
	/**
	 * get the list of methods in the app
	 * @param classes
	 * @return
	 */
	private static Set<SootMethod> getMethods()
	{
		Set<SootMethod> methods = new HashSet<SootMethod>();
		Chain<SootClass> chain = Scene.v().getApplicationClasses();
		for(SootClass sootClass: chain)
		{
			List<SootMethod> mlist = sootClass.getMethods();
			methods.addAll(mlist);}
		return methods;
	}
	static boolean unitBelongList(Unit u, List<Unit> g)
	{
		for(Unit i:g){
			if(i.equals(u))
				return true;}
		return false;
	}
}
