import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
 
public class FileParseJson {
    public static void main(String[] args) {
        try {
            String JsonContext = new Util().ReadFile("C:\\myWork\\SettingPattern\\target\\apkinfo.json");
            JSONObject rootObject = new JSONObject(JsonContext); // Parse the JSON to a JSONObject
            JSONArray patterns = rootObject.getJSONArray("pattern1"); // Get all JSONArray rows
 
            for(int j=0; j < patterns.length(); j++) { // Iterate each element in the elements array
                JSONObject pattern =  patterns.getJSONObject(j); // Get the element object
                JSONArray mainapis = pattern.getJSONArray("mainapi"); // Get duration sub object
                for(int i=0; i < mainapis.length(); i++) {
                    JSONObject mainapi =  mainapis.getJSONObject(i);
                    System.out.println("Classname: " + mainapi.getString("classname"));
                    System.out.println("Methodname: " + mainapi.getString("methodname"));
                }

                
                // JSONObject distance = element.getJSONObject("distance"); // Get distance sub object
                
                 // Print int value
                // System.out.println("Distance: " + distance.getInt("value")); // Print int value
            }
        } catch (JSONException e) {
            // JSON Parsing error
            e.printStackTrace();
        }
    }
}