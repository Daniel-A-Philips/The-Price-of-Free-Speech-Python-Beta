package Java;
import java.time.*;
import java.util.*;
import java.io.*;
import java.net.*;

public class FinnHub {

    private String Interval;
    private String Ticker;
    private String Format = "csv";
    protected int numDays = 0;
    private boolean forSMVI;


    protected ArrayList<String> RawData = new ArrayList<String>();
    protected ArrayList<String> ParsedData = new ArrayList<String>();
    protected ArrayList<String> Time = new ArrayList<String>();
    protected ArrayList<Double> Open = new ArrayList<Double>();
    protected ArrayList<Double> High = new ArrayList<Double>();
    protected ArrayList<Double> Low = new ArrayList<Double>();
    protected ArrayList<Double> Close = new ArrayList<Double>();
    protected ArrayList<Double> Volume = new ArrayList<Double>();


    protected ArrayList<LocalDate[]> Dates = new ArrayList<LocalDate[]>();
    private final String[] tempMonthArray = new String[] {"" ,"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};

    String[] start_end = new String[2];

    /**
     * Runs on the creation of the instance
     * Gathers and keeps track of data for a given stock
     * @param start     The starting month and year, e.g. October 2020
     * @param end       The ending month and year, e.g. January 2021
     * @param Ticker    The ticker of the stock, e.g. AAPL
     * @param Interval  The interval for the data gathering in minutes, e.g. 15
     */
    FinnHub(String start, String end, String Ticker, String Interval, boolean forSMVI ){
        start_end[0] = start;
        start_end[1] = end;
        this.Ticker = Ticker.toUpperCase();
        this.Interval = Interval;
        this.forSMVI = forSMVI;
        Run();
    }


    private void Run(){
        try{
            ArrayList<long[]> times = getDates();
            for(long[] time : times){
                urlConnect(time[0],time[1]);
            }
            writeToCSV();
            makeArrayLists();
        } catch(Exception e){ System.out.println(e + " occured on line " + e.getStackTrace()[0].getLineNumber() + " in betaRun.FinnHub.java");}
    }

    private void urlConnect(long start, long end){
        System.out.println("Connecting to URL");
        try{
            URL url = new URL("https://finnhub.io/api/v1/stock/candle?symbol=" + Ticker + "&resolution=" + Interval + "&from=" + start + "&to=" + end + "&format=" + Format + "&token=c1vv82l37jkoemkedus0");
            InputStream in = url.openStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));
            String line;
            ArrayList<String> temp = new ArrayList<String>();
            while((line = reader.readLine()) != null) {
                if(RawData.contains(line)) continue;
                //temp.add(line);
                RawData.add(line);
            }
            //temp.addAll(RawData);
            //RawData = temp;
        } catch(Exception e){ System.out.println(e + " occured on line " + e.getStackTrace()[0].getLineNumber() + " in urlConnect.FinnHub.java");}
    }

    private ArrayList<long[]> getDates(){
        ArrayList<long[]> holder = new ArrayList<long[]>();
        try{
            String a = start_end[0];
            String b = start_end[1];
            ArrayList<String> months = new ArrayList<String>(Arrays.asList(tempMonthArray));
            System.out.println("Created Lists");
            /* Run if only one month is selected */
            if(a.equals(b)){
                int year = Integer.parseInt(a.substring(a.length()-4,a.length()));
                System.out.println("One month is selected");
                System.out.println("line 90 of FinnHub.java");
                int month = months.indexOf(a.substring(0,a.length()-5));
                System.out.println("year : " + year + ", month : " + month);
                YearMonth temp = YearMonth.of(year,month);
                LocalDate date1 = LocalDate.of(year,month,1);
                LocalDate date2 = LocalDate.of(year,month,temp.lengthOfMonth());
                numDays += temp.lengthOfMonth();
                Dates.add(new LocalDate[]{date1,date2});
                holder.add(new long[]{toUnix(date1),toUnix(date2)});
                return holder;
            }

            int year1 = Integer.parseInt(a.substring(a.length()-4,a.length()));
            int year2 = Integer.parseInt(b.substring(b.length()-4,b.length()));

            int month1 = months.indexOf(a.substring(0,a.length()-5));
            int month2 = months.indexOf(b.substring(0,b.length()-5));
            
            int timesToRun;
            if(year2 != year1) timesToRun = month2 + (12-month1);
            else timesToRun = month2-month1;

            boolean isPreviousYear = false;
            boolean hasChangedYear = false;
            for(int i = 0; i <= timesToRun; i++){
                if(isPreviousYear & !hasChangedYear){
                    month2 = 12+i;
                    year2 = year1;
                    isPreviousYear = true;
                    hasChangedYear = true;
                }
                if(month2-i == 1){
                    isPreviousYear = true;
                }
                LocalDate date1 = LocalDate.of(year2,month2-i,1);
                YearMonth temp = YearMonth.of(year2,month2-i);
                LocalDate date2 = LocalDate.of(year2,month2-i,temp.lengthOfMonth());
                Dates.add(new LocalDate[]{date1,date2});
                holder.add(new long[]{toUnix(date1),toUnix(date2)});
            }
            for(long[] arr : holder){
                System.out.format("start : %d%n       end : %d%n", arr[0],arr[1]);
            }
        }   catch(Exception e) { System.out.println(e + " occured on line " + e.getStackTrace()[0].getLineNumber() + " in getDates.FinnHub.java");}
        return holder;
    }

    private long toUnix(LocalDate date){ 
        ZoneId zoneId = ZoneId.systemDefault();
        long epoch = date.atStartOfDay(zoneId).toEpochSecond();
        return epoch;
    }
    /**
     * Uses the data collected and stored in 'RawData' to format and write to the csv file
     */
    private void writeToCSV(){
        ArrayList<String> LinesToWrite = new ArrayList<String>();
        String csvPath;
        if(forSMVI) csvPath = "Data//DIA_Data.csv";
        else csvPath = "Data//Data.csv";
        try{
            System.out.println("writeToCSV");
            String line;
            File tempFile = new File(csvPath);
            FileWriter writer = new FileWriter(tempFile);
            String ogHeaders = "t,o,h,l,c,v";
            String headers = "time,open,high,low,close,volume";
            RawData.set(0,headers);
            for(int i = 1; i < RawData.size(); i++){
                line = RawData.get(i);
                if(line.equals(ogHeaders)) continue;
                if(!line.equals(headers)){
                    long unix = Long.parseLong(line.substring(0,line.indexOf(",")));
                    Date date = new Date();
                    date.setTime((long)unix*1000);
                    /* Comment the line below to change the date formatting to UNIX */
                    line = date + line.substring(line.indexOf(","),line.length());
                }
                RawData.set(i,line);
                LinesToWrite.add(line);
            }

            Collections.reverse(LinesToWrite);
            ArrayList<ArrayList<String>> allMonths = new ArrayList<>();
            ArrayList<String> month = new ArrayList<>();
            String currentMonth = "Mar";
            for(int i = 0; i < LinesToWrite.size(); i++){
                if(i == LinesToWrite.size()-1){
                    Collections.reverse(month);
                    allMonths.add(month);
                    month = new ArrayList<>();
                    currentMonth = LinesToWrite.get(i).substring(4,8);
                    //System.out.println(currentMonth);
                    month.add(LinesToWrite.get(i));
                    break;
                }
                if(LinesToWrite.get(i).contains(currentMonth)){
                    month.add(LinesToWrite.get(i));
                }else{
                    Collections.reverse(month);
                    allMonths.add(month);
                    month = new ArrayList<>();
                    currentMonth = LinesToWrite.get(i).substring(4,8);
                    month.add(LinesToWrite.get(i));
                }
            }
            LinesToWrite.clear();
            ArrayList<String> temp = new ArrayList<>();
            for(ArrayList<String> a : allMonths){
                temp.addAll(a);
            }
            LinesToWrite = temp;
            LinesToWrite.add(0,"time,open,high,low,close,volume");
            System.out.println("LinesToWrite.size() :" + LinesToWrite.size());
            for(int i = 0; i < LinesToWrite.size(); i++){
                writer.write(LinesToWrite.get(i)+"\n");
            }
            writer.close();
            ParsedData.addAll(LinesToWrite);
        }catch(IOException e){System.out.println(e + " occured on line " + e.getStackTrace()[0].getLineNumber() + " in writeToCSV.FinnHub.java");}
    }

    /**
     * Uses parsed data and adds that data to individual protected ArrayLists for access from other classes
     */
    private void makeArrayLists(){
        System.out.println("Making ArrayLists");
        for(String s : ParsedData){
            if(s.contains("w")) continue;
            String[] raw = s.split(",");
            Time.add(raw[0]);
            Open.add(Double.parseDouble(raw[1]));
            High.add(Double.parseDouble(raw[2]));
            Low.add(Double.parseDouble(raw[3]));
            Close.add(Double.parseDouble(raw[4]));
            Volume.add(Double.parseDouble(raw[5]));
        }
        System.out.println("Finished ArrayLists");
    }
}
