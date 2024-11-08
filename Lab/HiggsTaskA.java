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

public class HiggsTaskA
{
    // Declare constants and parameters

       public static  int[] NM= new int[1500];
       public static  double[] BackgroundFit= new double[300];

    
    // Start main method
    public static void main(String[] args)
    {

       


        ////////////////////////////////////////////////////////////////////////
        //1.  read from the events data file
        ////////////////////////////////////////////////////////////////////////
        
	//String filename = "diphotonevents.lhco";
	//String filename = "tag_1_pgs_events.lhco";
        String filename = "TenEvents.dat";

        // Open the file
        File file = new File(filename);



	try
	    {   BufferedReader in = new BufferedReader(new FileReader(file));  // we use bufferedreader to read the file 
	   
	System.out.println("File open successful!");

	
	    int line = 0; // line in the data file
	    int event = 0; // number of event
	    int nphoton =0; // photon number in event (1 or 2 or maybe 3)
	    double[] ETA = new double[8]; 
	    double[] PHI = new double[8]; // kinematic variables of particles
	    double[] PT = new double[8];

		    
            for (String x = in.readLine(); x != null; x = in.readLine())  // "for-loop" reading a line at a time
		{ line++;
		    String presstr1 = x.substring(0,1);   //  read the first character of the line 
		   
		    if (presstr1.equals("#") ) {}  //System.out.println(x);}  // if it is "#" then do NOTHING
		    else{  
			String sstr = x.substring(2,3); // read the third character of the line
 
		       if(sstr.equals("#")){} // if it is  "#" , then do NOTHING
		       else if(sstr.equals("0")) {nphoton=0; event++; } //if it is 0 then it is a new event. Also reset photon counter
			   else
			       {  String stp = x.substring(7,8); //read the 8 character
			       int type = Integer.parseInt(stp); //convert string to integer - particle type;
			       if(type==0){ // type= 0 is a photon then read eta, phi and pt for it
			                String seta= x.substring(11,17); double eta = Double.parseDouble(seta);
					   // read eta of photon
					String sphi= x.substring(19,24);double phi = Double.parseDouble(sphi);
					   // read phi of photon			      
					String spt= x.substring(27,32);double pt = Double.parseDouble(spt);
					   // read pt of photon			       
					System.out.println(eta+" " + " "+ phi +" " +" "+ pt);
					if(pt > 15){nphoton++;
 						ETA[nphoton]=eta;
						PHI[nphoton]=phi;
						PT[nphoton]=pt;
						    }
				        if(nphoton>=4){ System.out.println("4 or more photon in event " + event);}
					if(nphoton==2){ // whenever there are two photons, compute their invariant mass 



					    ///////////////////////////////////////////
					    // you need to write something here!!!!!!!!
					    /////////////////////////////////////////////
					    	        double M = 0.00;
					    //////////////////////////////////////////////
						
						System.out.println("invariant mass = " +M);

						
						       }
					if(nphoton==3){// when there are three photons
						//System.out.println("in event " + event + "  eta1= "+ ETA[1] + ", eta2= " +ETA[2]);

					                 double M12 =   0.00;
						// you need to write something here!!!!!!!!
						//System.out.println("round invariant mass = " +M12);

						// you need to write something here!!!!!!!!
					                  double M23 =   0.00;
					    
					    //System.out.println("round invariant mass = " +M23);
					        // you need to write something here!!!!!!!!
							double M13 =   0.00;
						//System.out.println("round invariant mass = " +M13);
						
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

 




	
    }
}
