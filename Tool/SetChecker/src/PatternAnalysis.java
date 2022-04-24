
import soot.Value;
import soot.Unit;
import soot.jimple.*;
import soot.toolkits.graph.DirectedGraph;
import soot.toolkits.scalar.ForwardFlowAnalysis;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * @program: MySootScript
 * @description:
 * @author: Dr.Navid
 * @create: 2021-05-10 15:11
 **/


public class PatternAnalysis extends ForwardFlowAnalysis<Unit, PatternFlowSet> {


    public enum AnalysisMode {MUST, MAY_P, MAY_O}

    public AnalysisMode analysisMode;
    PatternFlowSet newset = new PatternFlowSet();
    JSONArray flowgens ,flowkills;

    

    public PatternAnalysis(DirectedGraph graph, PatternFlowSet newset, JSONArray flowgens, JSONArray flowkills) {
        super(graph);
        this.analysisMode = AnalysisMode.MUST;
        this.newset = newset;
        this.flowgens = flowgens;
        this.flowkills = flowkills;

        doAnalysis();
    }

    @Override
    protected PatternFlowSet entryInitialFlow() {
        return this.newset;
    }

    @Override
    protected void flowThrough(PatternFlowSet inSet, Unit unit, PatternFlowSet outSet) {
        inSet.copy(outSet);
        kill(inSet, unit, outSet);
        gen(inSet, unit, outSet);
    }

    @Override
    protected void merge(PatternFlowSet inSet1, PatternFlowSet inSet2, PatternFlowSet outSet) {
        inSet1.union(inSet2, outSet);
    }

    @Override
    protected void copy(PatternFlowSet source, PatternFlowSet dest) {
        //Copies the current FlowSet into dest.
        source.copy(dest);
    }

    protected void kill(PatternFlowSet inSet, Unit unit, PatternFlowSet outSet){
        if(unit.toString().contains("requireNonNull")){
            System.out.println(unit);
        }
        unit.apply(new AbstractStmtSwitch() {
            @Override
            public void caseAssignStmt(AssignStmt stmt) {
                Value rightOp = stmt.getRightOp();
                for(int i=0; i < flowkills.length(); i++) {
                    if(unit.toString().contains(flowkills.getJSONObject(i).getString("methodname"))
                    && unit.toString().contains(flowkills.getJSONObject(i).getString("classname"))){
                        // System.out.println("stmt:"+stmt.toString());
                        for(Value v:inSet){
                            if (rightOp.toString().contains(v.toString())){
                                // System.out.println("special:"+v.toString());
                                outSet.remove(v);
                            }
                        }
                    }
                }
            }
            @Override
            public void caseIfStmt(IfStmt stmt) {
                Value condition = stmt.getCondition();
                for(int i=0; i < flowkills.length(); i++) {
                    if(unit.toString().contains(flowkills.getJSONObject(i).getString("methodname")) 
                    && unit.toString().contains(flowkills.getJSONObject(i).getString("classname"))){
                        // System.out.println("stmt:"+stmt.toString());
                        for(Value v:inSet){
                            if (condition.toString().contains(v.toString())){
                                // System.out.println("special:"+v.toString());
                                outSet.remove(v);
                            }
                        }
                    }
                }
            }
        });
    }

    protected void gen(PatternFlowSet inSet, Unit unit, PatternFlowSet outSet){
        
        unit.apply(new AbstractStmtSwitch() {
            @Override
            public void caseAssignStmt(AssignStmt stmt) {
                
                Value leftOp = stmt.getLeftOp();
                Value rightOp = stmt.getRightOp();
                for(int i=0; i < flowgens.length(); i++) {
                    String gen_class = flowgens.getJSONObject(i).getString("classname");
                    String gen_method = flowgens.getJSONObject(i).getString("methodname");
                    if(rightOp.toString().contains(gen_method) && rightOp.toString().contains(gen_class)){
                        // System.out.println(unit.toString());
                        outSet.add(leftOp);
                    }
                }
            }
            @Override
            public void caseIdentityStmt(IdentityStmt stmt) {
                Value leftOp = stmt.getLeftOp();
                Value rightOp = stmt.getRightOp();
                for(int i=0; i < flowgens.length(); i++) {
                    String gen_method = flowgens.getJSONObject(i).getString("methodname");
                    if(rightOp.toString().contains(gen_method)
                    && rightOp.toString().contains(flowgens.getJSONObject(i).getString("classname"))){
                    System.out.println(unit.toString());
                        outSet.add(leftOp);
                    }
                }
            }
        });
    }

    @Override
    protected PatternFlowSet newInitialFlow() {
        // TODO Auto-generated method stub
        return new PatternFlowSet();
    }
}
