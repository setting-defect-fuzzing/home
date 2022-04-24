
import soot.toolkits.scalar.AbstractBoundedFlowSet;
import soot.Value;

import java.util.*;

/**
 * @program: MySootScript
 * @description:
 * @author: 0range
 * @create: 2021-05-10 18:54
 **/


public class PatternFlowSet extends AbstractBoundedFlowSet<Value> {

    private Set<Value> liveVariableSet = new HashSet<>();
    public PatternFlowSet(){
        super();
    }

    @Override
    public PatternFlowSet clone() {
        PatternFlowSet myClone = new PatternFlowSet();
        myClone.liveVariableSet.addAll(this.liveVariableSet);
        return myClone;
    }

    @Override
    public boolean isEmpty() {
        return liveVariableSet.isEmpty();
    }

    @Override
    public int size() {
        return liveVariableSet.size();
    }

    @Override
    public void add(Value local) {
        liveVariableSet.add(local);
    }

    @Override
    public void remove(Value local) {
        if(liveVariableSet.contains(local)) {
            liveVariableSet.remove(local);
        }
    }

    @Override
    public boolean contains(Value local) {
        return liveVariableSet.contains(local);
    }

    @Override
    public Iterator<Value> iterator() {
        return liveVariableSet.iterator();
    }

    @Override
    public List<Value> toList() {
        return new ArrayList<>(liveVariableSet);
    }
}
