

double average(vector<double>);
double error(vector<double>);



void IV()
{
 ifstream infile;
 TH1D::SetDefaultSumw2();
 double current, voltage, temp;
 auto c1 =new TCanvas("c1","Canvas",200,10,800,800);
 TGaxis::SetMaxDigits(3);
 std::unique_ptr<TFile> myFile( TFile::Open("IV-Histos.root", "RECREATE") );
 char filename[29][55]={"Si_SiO2_W_filmT-2.300000H-0.000000 111025_150616.txt",
"Si_SiO2_W_filmT-2.400000H-0.000000 111025_150337.txt",
"Si_SiO2_W_filmT-2.500000H-0.000000 111025_150022.txt",
"Si_SiO2_W_filmT-2.600000H-0.000000 111025_145748.txt",
"Si_SiO2_W_filmT-2.700000H-0.000000 111025_145407.txt",
"Si_SiO2_W_filmT-2.800000H-0.000000 111025_145137.txt",
"Si_SiO2_W_filmT-2.900000H-0.000000 111025_144908.txt",
"Si_SiO2_W_filmT-3.000000H-0.000000 111025_143845.txt",
"Si_SiO2_W_filmT-3.100000H-0.000000 111025_143616.txt",
"Si_SiO2_W_filmT-3.200000H-0.000000 111025_143348.txt",
"Si_SiO2_W_filmT-3.300000H-0.000000 111025_143120.txt",
"Si_SiO2_W_filmT-3.400000H-0.000000 111025_142852.txt",
"Si_SiO2_W_filmT-3.500000H-0.000000 111025_142624.txt",
"Si_SiO2_W_filmT-3.600000H-0.000000 111025_142249.txt",
"Si_SiO2_W_filmT-3.700000H-0.000000 111025_142021.txt",
"Si_SiO2_W_filmT-3.800000H-0.000000 111025_141752.txt",
"Si_SiO2_W_filmT-3.900000H-0.000000 111025_141524.txt",
"Si_SiO2_W_filmT-4.000000H-0.000000 111025_141257.txt",
"Si_SiO2_W_filmT-4.100000H-0.000000 111025_141028.txt",
"Si_SiO2_W_filmT-4.200000H-0.000000 111025_140759.txt",
"Si_SiO2_W_filmT-4.300000H-0.000000 111025_140529.txt",
"Si_SiO2_W_filmT-4.400000H-0.000000 111025_140301.txt",
"Si_SiO2_W_filmT-4.500000H-0.000000 111025_140033.txt",
"Si_SiO2_W_filmT-4.600000H-0.000000 111025_135804.txt",
"Si_SiO2_W_filmT-4.700000H-0.000000 111025_135535.txt",
"Si_SiO2_W_filmT-4.800000H-0.000000 111025_135302.txt",
"Si_SiO2_W_filmT-4.900000H-0.000000 111025_135035.txt",
"Si_SiO2_W_filmT-5.000000H-0.000000 111025_134755.txt",
"Si_SiO2_W_filmT-300.000000H-0.000000 111025_121633.txt"
		      };
 double Cvalues[11]={-5,-4,-3,-2,-1,0.0,1,2,3,4,5};
 double Tc[11][2]={{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0},{0,0}};
 double Rthresh[2]={50,5000};

 TGraphErrors *RTgraph=new TGraphErrors[10]();
 //{TGraph("R vs T with current -0.5 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current -0.4 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current -0.3 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current -0.2 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current -0.1 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current 0.1 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current 0.2 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current 0.3 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current 0.4 mA; Temperature (K); Resistance (m#Ohm)"),TGraph("R vs T with current 0.5 mA; Temperature (K); Resistance (m#Ohm)")};
 for(int i=0,mod=0;i<11;i++)
 {
  if(i==5){mod=1;continue;}
  RTgraph[i-mod].SetTitle(string("R vs T with current ")+Cvalues[i]+" mA; Temperature (K); Resistance (m#Omega)");
 }
 for(int i=2,j=3;float(i)+float(j)/10<=5;j++)
 {
  int itemp=i+j/10, jtemp=j%10;
  //cout<<string("file")+itemp+"."+jtemp+"\n";
  //TH1D *IV_hist= new TH1D("",string("I-V characteristics at ")+itemp+"."+jtemp+" K; Current (mA); Voltage (#mu V)",13,-6,6);
  //infile.open(string("Si_SiO2_W_filmT-")+itemp+"."+jtemp+"00000H-0.000000*.txt");
  infile.open(filename[j-3]);
  if(!infile.good()){cout<<"Error opening file\n";break;}
  vector<double> Vvalues[11];
  auto graph = new TGraphErrors();
  while(infile>>current>>voltage>>temp>>temp)
   for(int k=0;k<11;k++)
//    if(abs(values[0][i]-current*1e3)<0.001)
    if(Cvalues[k]==current*1e3)
    {
     Vvalues[k].push_back(voltage*1e6);
    }
  for(int k=0,mod=0;k<11;k++)
  {
   graph->AddPointError(Cvalues[k],average(Vvalues[k]),0,error(Vvalues[k]));
   if(k==5){mod=1;continue;}
   RTgraph[k-mod].AddPointError(float(i)+float(j)/10,fabs(average(Vvalues[k])/Cvalues[k]),0,error(Vvalues[k])/(Cvalues[k]*Cvalues[k]));
   if(Rthresh[0]>fabs(average(Vvalues[k])/Cvalues[k]))
    Tc[k-mod][0]=float(i)+float(j)/10;
   if((Rthresh[1]<fabs(average(Vvalues[k])/Cvalues[k]))&&(Tc[k-mod][1]==0))
    Tc[k-mod][1]=float(i)+float(j)/10;
  }
//  if(float(i)+float(j)/10>=4)graph->GetYaxis()->SetRangeUser(-6e4,6e4);
  graph->SetTitle(string("I-V characteristics at ")+itemp+"."+jtemp+" K; Current (mA); Voltage (#mu V)");
  graph->SetMarkerStyle(21);
  graph->GetYaxis()->SetTitleOffset(1.2);
  graph->Draw("ALP");
 // IV_hist->Fill(current*1e3,voltage*1e6);
 // IV_hist->Draw("ep");
  c1->SaveAs(string("I-V-T_")+itemp+"."+jtemp+"K.pdf");
  c1->Clear();
  myFile->WriteObject(graph,string("I-V characteristics at ")+itemp+"."+jtemp+" K");
  infile.close();
 }
 infile.open(filename[28]);
 if(!infile.good()){cout<<"Error opening file\n";return;}
  //double Cvalues[11]={-5,-4,-3,-2,-1,0.0,1,2,3,4,5};
  vector<double> Vvalues[11];
  auto graph = new TGraphErrors();
  while(infile>>current>>voltage>>temp>>temp)
   for(int i=0;i<11;i++)
//    if(abs(values[0][i]-current*1e3)<0.001)
    if(Cvalues[i]==current*1e3)
    {
     Vvalues[i].push_back(voltage*1e6);
    }
  for(int i=0;i<11;i++)
  {
   graph->AddPointError(Cvalues[i],average(Vvalues[i]),0,error(Vvalues[i]));
  }
  graph->SetTitle("I-V characteristics at 300 K; Current (mA); Voltage (#mu V)");
  graph->SetMarkerStyle(21);
  graph->GetYaxis()->SetTitleOffset(1.2);
//  graph->GetYaxis()->SetRangeUser(-6e4,6e4);
  graph->Draw("ALP");
 // IV_hist->Fill(current*1e3,voltage*1e6);
 // IV_hist->Draw("ep");
  c1->SaveAs("I-V-T_300K.pdf");
  c1->Clear();
  infile.close();
  c1->SetLogy();
  TGraphErrors *ITc=new TGraphErrors();
  for(int i=0,mod=0;i<11;i++)
  {
   if(i==5){mod=1;continue;}
   RTgraph[i-mod].SetMarkerStyle(21);
   RTgraph[i-mod].GetYaxis()->SetTitleOffset(1.2);
   RTgraph[i-mod].GetYaxis()->SetRangeUser(1e-2,5e4);
   RTgraph[i-mod].Draw("ALP");
   c1->SaveAs(string("R-T-I_")+Cvalues[i]+"A.pdf");
   c1->Clear();
   myFile->WriteObject(&RTgraph[i-mod],string("R vs T with current ")+Cvalues[i]+" mA");
   ITc->AddPointError(Cvalues[i-mod],(Tc[i-mod][0]+Tc[i-mod][1])/2,0,0.05);
   cout<<Tc[i-mod][0]<<'\t'<<Tc[i-mod][1]<<endl;
  }
  c1->SetLogy(0);
  ITc->SetTitle("Transition temperature vs bias current;Current (mA);T_{c} (K)"); 
  ITc->SetMarkerStyle(21);
  ITc->GetYaxis()->SetTitleOffset(1.4);
  ITc->Draw("ALP");
  c1->SaveAs("Tc-vs-I.pdf");
  c1->Clear();
}

double average(vector<double> values)
{
 double sum=0;
 for(int i=0;i<values.size();i++)
  sum+=values[i];
  return (values.size()!=0)?sum/values.size():0;
}

double error(vector<double> values)
{
 double ssum=0,avg=average(values);
 for(int i=0;i<values.size();i++)
  ssum+=(values[i]-avg)*(values[i]-avg);
  //cout<<ssum/(values.size()-1)<<"\t"<<sqrt(ssum/(values.size()-1))<<endl;
  return ((values.size()-1)!=0)?sqrt(ssum/(values.size()-1)):0;
}
