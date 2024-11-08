/**
 Lab 5
Manuel Toharia, Joel Trudeau
 Current version written: April 2018
 Description: Higgs to diphotons, bump hunting, statistics, large datasets
 */

// Import packages
import java.io.*;
import java.awt.*;
import javax.swing.*;
import java.util.Scanner;
import org.apache.commons.math3.fitting.*;
//import org.math.plot.*;
//import org.math.plot.plotObjects.*;
import java.util.Arrays;

public class HiggsTaskB
{
    // Declare constants and parameters

    public static  int[] NM= new int[1500];  //Bin counters for histogram
    public static  double[] BackgroundFit= new double[300]; // array for the interpolation


    
    // Start main method
    public static void main(String[] args)
    {

       


        ////////////////////////////////////////////////////////////////////////
        //1.  read from the events data file
        ////////////////////////////////////////////////////////////////////////
        
	//String filename = "diphotonevents.lhco";
	String filename = "DiphotonsA.dat";
       

        // Open the file
        File file = new File(filename);

        // buffersize
	//	int buffersize = 16*1024;

	try
	    {   BufferedReader in = new BufferedReader(new FileReader(file));//,buffersize); 
	   
	System.out.println("File open successful!");

	
	    int line = 0; // line in the data file
	    int event = 0; // number of event
	    int nphoton =0; // photon number in event (1 or 2 or maybe 3)
	    double[] ETA = new double[8]; 
	    double[] PHI = new double[8]; // kinematic variables of particles
	    double[] PT = new double[8];


	    for(int i=0; i<=70; i++) {NM[90+2*i]=0;} //set to zero the bin counters


	    
            for (String x = in.readLine(); x != null; x = in.readLine()) 
		{ line++;
		    String presstr1 = x.substring(0,1); 
		    if (presstr1.equals("#") ) {}  // Do NOTHING
		    else{ 
		       String sstr = x.substring(2,3);		       
		       if(sstr.equals("#")){}      //Do Nothing
		       else if(sstr.equals("0")) {nphoton=0; event++; } //new event, reset photon counter
			   else
		       {   String stp = x.substring(7,8);
			    int type = Integer.parseInt(stp);// convert string to integer
			   if(type==0){  // type= 0 is a photon
			                String seta= x.substring(11,17); double eta = Double.parseDouble(seta);
				    	 // read eta of photon
					String sphi= x.substring(19,24);double phi = Double.parseDouble(sphi);
					 // read phi of photon			      
					String spt= x.substring(27,32);double pt = Double.parseDouble(spt);
					 // read pt of photon			       
					
					if(pt > 15){nphoton++;
 						ETA[nphoton]=eta; PHI[nphoton]=phi; PT[nphoton]=pt;
						    }
				        if(nphoton>=3){ System.out.println("3 or more photon in event " + event);}
					if(nphoton==2){
						
					        double M = Math.sqrt(2*PT[1]*PT[2]*(Math.cosh(ETA[1]-ETA[2])-Math.cos(PHI[1]-PHI[2])));
						


						////////////////////////////////////////////////////////////
						//Need to do something here!!!!!!
						int Mround=0; // ROUND the mass to an even integer to make the histogram
						////////////////////////////////////////////



						

						NM[Mround]=NM[Mround]+1;  // increase the bin counter for that mass
						       }
					 if(nphoton==3){
						//System.out.println("in event " + event + "  eta1= "+ ETA[1] + ", eta2= " +ETA[2]);
					        
					
						double M23 = Math.sqrt(2*PT[2]*PT[3]*(Math.cosh(ETA[2]-ETA[3])-Math.cos(PHI[2]-PHI[3])));

						////////////////////////////////////////////////////////
						int Mround23=0; System.out.println("I forgot to implement something");
										   // do something... round to an even integer
						////////////////////////////////////////////////////////
						NM[Mround23]=NM[Mround23]+1;
					
						double M13 = Math.sqrt(2*PT[1]*PT[3]*(Math.cosh(ETA[1]-ETA[3])-Math.cos(PHI[1]-PHI[3])));

						
						/////////////////////////////////////////////////////////
						int Mround13=0;// Do something!!!!! round to an even integer
						////////////////////////////////////////////////////////
						
						NM[Mround13]=NM[Mround13]+1;
					
						        }
			             }
		       }

  		       
		    } 
            }




	} catch (IOException e)
        {
            System.out.println("File I/O error!");
        }
	
	///
	//2. Counting - mass bin results histogram output

  for(int i=0; i<=70; i++) {System.out.println(NM[90+2*i]+ " diphoton events with invariant mass " + (90+2*i) ) ;}

 
  
      //////////////////////////////////////////////////////////////
        // 3. Opening a file to store data
        ////////////////////////////////////////////////////////////////////////
        String filename2 = "massdistribution.dat";
        PrintWriter outputFile = null;

        try
        {
            outputFile = new PrintWriter(new FileOutputStream(filename2,false));
        }
        catch(FileNotFoundException e)
        {
            System.out.println("File error.  Program aborted.");
            System.exit(0);
        }


        ////////////////////////////////////////////////////////////////////////
        //2. print mass bin results to file 
        ////////////////////////////////////////////////////////////////////////
   
      

	for(int i=0; i<=67; i++) {	outputFile.printf((90+2*i) + " " + NM[90+2*i] +  "%n" );}



        ////////////////////////////////////////////////////////////////////////
        //4.  Clean up after yourself!
        ////////////////////////////////////////////////////////////////////////
        // ALWAYS, ALWAYS close your file before exiting!
        outputFile.close();







	
    }
}
