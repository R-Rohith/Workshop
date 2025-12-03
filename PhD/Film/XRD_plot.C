int XRD_plot()
{
 ifstream fin;
 fin.open("filelist.txt");
 //if(!fin.is_open()) return 1;
 
 char filename[50];
 char plotname[50];
 TFile *outfile= new TFile("XRD.root","RECREATE");
 while(fin>>filename)
 {
  ifstream datafile;
  datafile.open(filename);
  if(!datafile.is_open()) return 1;
  
  double x, y;
  TGraphErrors *XRDgraph= new TGraphErrors();
  strcpy(plotname,filename);
  strcat(plotname,"_XRD;2#theta;Intensity");
  XRDgraph->SetTitle(plotname);
  while(datafile>>x>>y)
   XRDgraph->AddPointError(x,y,0,0);
  
  strcpy(plotname,filename);
  strcat(plotname,"XRD plot");
  outfile->WriteObject(XRDgraph,plotname);
  datafile.close();
 }
 fin.close();
 outfile->Close();
 return 0;
}
