package Java;
import java.io.*;
import java.time.Month;
import java.util.*;


public class Interaction {
    private String Ticker;
    private int IntervalIndex;
    private String Interval;
    private String StartSlice;
    private String EndSlice;
    private String Handle;
    private boolean forSMVI;
    private StockBeta stock;
    protected static ArrayList<String> allSlices = new ArrayList<String>();


    public Interaction(String Ticker, int IntervalIndex, String StartSlice, String EndSlice, String Handle, boolean forSMVI) throws IOException {
        this.Ticker = Ticker;
        this.IntervalIndex = IntervalIndex;
        this.StartSlice = StartSlice;
        this.EndSlice = EndSlice;
        this.Handle = Handle;
        this.forSMVI = forSMVI;
    }

    public void run(){
        try{
            System.out.println("Running Interaction");
            parseTicker();
            parseInterval();
            writeHandles();
            System.out.println("created stock");
            stock = new StockBeta(Ticker, Interval, StartSlice, EndSlice, forSMVI);
            System.out.print("Day SD of " + Ticker + ": " + stock.DayDeviation());
            System.out.println("Daily Average of " + this.Ticker + ": " + stock.avgDayPrice());
        } catch(Exception e){
            System.out.println("Error in Interaction.run()");
            System.err.println(e + e.getLocalizedMessage());}
    }

    private void parseTicker(){
        Ticker = Ticker.replaceAll("\\s","").toUpperCase();
        System.out.println("parsed Ticker");
    }

    private void parseInterval() {
        String[] stringOptions = new String[]{"1","5","15","30","60"};
        Interval = stringOptions[IntervalIndex];
        System.out.println("parsed Interval");
    }

    private void print(String data){
        System.out.println("Started print");
        gui.WriteText(data);
    }

    private void writeHandles(){
        if(forSMVI) return;
        try{
            File file = new File(gui.absPath + "Handles.csv");
            FileWriter writer = new FileWriter(file);
            Handle = Handle.replaceAll("\\s+","");
            String[] Handles = Handle.split(",");
            writer.write("Handle,ID\n");
            for(String s : Handles){
                writer.write(s+"\n");
            }
            writer.close();
        }catch(Exception e){System.out.println(e);}
    }

    public int getNumberOfDataPoints(){
        return stock.RawData.size()-1;
    }

    public ArrayList<String[]> getRawData(){
        return stock.RawData;
    }

    public double getVariation(ArrayList<String[]> a){
        return stock.getVariation(a);
    }
}
