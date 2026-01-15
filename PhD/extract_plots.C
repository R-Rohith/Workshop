
	auto c1 = new TCanvas("c1","Canvas",200,10,800,800);

int extract_plots(char *filename,char *objectname,char *Objtype,char *stat)
{
  void OneD_hist(char*,char*,char*);
  void TwoD_GE(char*,char*,char*);
//  if(*argc!=5) return 1;

//	ROOT::EnableImplicitMT();
 std::cout<<Objtype<<endl;
 if(std::strcmp(Objtype,"TH1D")==0)
  OneD_hist(filename,objectname,stat);
 else if(std::strcmp(Objtype,"TGraphErrors")==0)
  TwoD_GE(filename,objectname,stat);
return 0;
}


void OneD_hist(char *filename,char *objectname,char *stat)
{
 std::cout<<"Plotting...";
 TFile *rootfile=TFile::Open(filename);
 TH1D *hist=(TH1D*)rootfile->Get(objectname);
 if(std::strcmp(stat,"FullStat")==0)
  gStyle->SetOptStat(111110);
 else if(std::strcmp(stat,"MinStat")==0)
  gStyle->SetOptStat(1110);
 else if(std::strcmp(stat,"NoStat")==0)
  gStyle->SetOptStat(0);
 
 c1->SetLogy();
 
 hist->GetXaxis()->SetLabelSize(0.05);
 hist->GetXaxis()->SetTitleSize(0.05);
 hist->GetXaxis()->SetTitleOffset(0.95);
 
 hist->GetYaxis()->SetLabelSize(0.05);
 hist->GetYaxis()->SetTitleSize(0.05);
 hist->GetYaxis()->SetTitleOffset(1.05);
 
 hist->Draw("ep");
 c1->Update();
 char str[100];
 strcpy(str,objectname);
 std::strcat(str,".pdf");
 c1->SaveAs(str);
 c1->Clear();
}

void TwoD_GE(char *filename,char *objectname,char *stat)
{
 std::cout<<"Plotting...";
 TFile *rootfile=TFile::Open(filename);
 TGraphErrors *graph=(TGraphErrors*)rootfile->Get(objectname);
 if(std::strcmp(stat,"FullStat")==0)
  gStyle->SetOptStat(111110);
 else if(std::strcmp(stat,"MinStat")==0)
  gStyle->SetOptStat(1110);
 else if(std::strcmp(stat,"NoStat")==0)
  gStyle->SetOptStat(0);
 
 c1->SetLogy();
 
 graph->GetXaxis()->SetLabelSize(0.05);
 graph->GetXaxis()->SetTitleSize(0.05);
 graph->GetXaxis()->SetTitleOffset(0.95);
 graph->GetXaxis()->SetRangeUser(20,80);
 
 graph->GetYaxis()->SetLabelSize(0.05);
 graph->GetYaxis()->SetTitleSize(0.05);
 graph->GetYaxis()->SetTitleOffset(0.9);
 
 graph->GetXaxis()->SetTitle("2#theta (deg)");
 graph->Draw("ALP");
 c1->Update();
 char str[100];
 strcpy(str,objectname);
 std::strcat(str,".pdf");
 c1->SaveAs(str);
 c1->Clear();
}

/*
theta_hist->Draw("ep");
	c1->SaveAs("theta-hist.pdf");
	c1->Clear();
	phi_hist->Draw("ep");
	c1->SaveAs("phi-hist.pdf");
	c1->Clear();
//	c1->SetLogy();
//        r_energy_hist->Draw("ep");
//        c1->SaveAs("recoil-energy-hist.pdf");
//        c1->Clear();
//        phononNo_hist->Draw("ep");
//        c1->SaveAs("phonon-number-hist.pdf");
//        c1->Clear();
//        lfactor_hist->Draw("ep");
//        c1->SaveAs("Lindhard-factor-hist.pdf");
//        c1->Clear();
//        c1->SetLogy(0);
        gStyle->SetPalette(1);
        gStyle->SetOptStat(0);
	vertex_hist->Draw();
	c1->SaveAs("Vertex-distribution-hist.pdf");
	c1->Clear();
	initial_dir_hist->Draw();
	c1->SaveAs("Initial-direction-hist.pdf");
	c1->Clear();
	xypos_hist->GetYaxis()->SetTitleOffset(1.2);
        xypos_hist->Draw("COLZ");
	gPad->Update();
        TPaletteAxis *palette = (TPaletteAxis*)xypos_hist->GetListOfFunctions()->FindObject("palette");
	palette->SetX1NDC(0.91);
	palette->SetX2NDC(0.93);
	palette->SetY1NDC(0.1);
	palette->SetY2NDC(0.9);
       	palette->SetLabelSize(0.03);
       	gStyle->SetTitleFontSize(0.07);
	gPad->Modified();
       	gPad->Update();
        c1->SaveAs("xy-distribution-hist.pdf");
        c1->Clear();
//        zpos_hist->Draw("COLZ");
//       	gPad->Update();
//	palette = (TPaletteAxis*)zpos_hist->GetListOfFunctions()->FindObject("palette");
//	palette->SetX1NDC(0.91);
//       	palette->SetX2NDC(0.93);
//       	palette->SetY1NDC(0.1);
//       	palette->SetY2NDC(0.9);
//       	palette->SetLabelSize(0.04);
//       	gStyle->SetTitleFontSize(0.07);
//       	gPad->Modified();
//       	gPad->Update();
//        c1->SaveAs("xz-distribution-hist.pdf");
//        c1->Clear();
	c1->SetLogz();
	TESxypos_hist->GetZaxis()->SetRangeUser(2e3,4e4);
	TESxypos_hist->GetYaxis()->SetTitleOffset(1.2);
	TESxypos_hist->Draw("COLZ");
        gPad->Update();
        TPaletteAxis *palette = (TPaletteAxis*)TESxypos_hist->GetListOfFunctions()->FindObject("palette");
        palette->SetX1NDC(0.91);
        palette->SetX2NDC(0.93);
        palette->SetY1NDC(0.1);
        palette->SetY2NDC(0.9);
        palette->SetLabelSize(0.03);
        gStyle->SetTitleFontSize(0.07);
        gPad->Modified();
        gPad->Update();
        c1->SaveAs("TES-xy-distribution-hist.pdf");
        c1->Clear();
	c1->SetLogz(0);
        gStyle->SetOptStat(1);

  TH1D *temperature_hist=new TH1D("","Expected temperature increase per event; T (K); Events",100,0,200);
  TH2D *temp_vs_x_hist= new TH2D("","Temperature increase vs primary vertex position (X); x (cm); T (#mu K); Events",100,-15,15,100,0,50);
  TH2D *temp_vs_y_hist= new TH2D("","Temperature increase vs primary vertex position (Y); y (cm); T (#mu K); Events",100,-15,15,100,0,50);
  TH2D *temp_vs_z_hist= new TH2D("","Temperature increase vs primary vertex position (Z); z (cm); T (#mu K); Events",100,-15,15,100,0,50);
  Double_t Get_temp(Double_t);
//  TH2D *edep_vs_Renergy =new TH2D("","Deposited energy vs recoil energy; Recoil energy (eV); Deposited energy (eV); Events",100,0,200,100,0,200);
  
	temperature_hist->Sumw2();
	temp_vs_x_hist->Sumw2();
	temp_vs_y_hist->Sumw2();
	temp_vs_z_hist->Sumw2();
  for(int i=0;i<event_count;i++)
  {						
	  temperature_hist->Fill(Get_temp(edep_arr[i])/1e6);
//	  cout<<Get_temp(edep_arr[i])<<endl;
//	  edep_vs_Renergy->Fill(r_energy_arr[i],edep_arr[i]);
	  temp_vs_x_hist->Fill(pos_arr[i][0],Get_temp(edep_arr[i]));
	  temp_vs_y_hist->Fill(pos_arr[i][1],Get_temp(edep_arr[i]));
	  temp_vs_z_hist->Fill(pos_arr[i][2],Get_temp(edep_arr[i]));
  }
  gStyle->SetOptStat(111110);
//  gStyle->SetOptStat(1110);
   c1->SetLogy();
 temperature_hist->Draw("ep");
  c1->SaveAs("Temperature-hist.pdf"); 
  c1->Clear();
        c1->SetLogy(0);
  gStyle->SetOptStat(0);
//  edep_vs_Renergy->Draw("COLZ");
// gPad->Update();
//palette = (TPaletteAxis*)edep_vs_Renergy->GetListOfFunctions()->FindObject("palette");
//palette->SetX1NDC(0.91);
// palette->SetX2NDC(0.93);
// palette->SetY1NDC(0.1);
// palette->SetY2NDC(0.9);
// palette->SetLabelSize(0.03);
// gStyle->SetTitleFontSize(0.07);
// gPad->Modified();
// gPad->Update();
// c1->SaveAs("recoil-vs-deposited.pdf"); 
//  c1->Clear();
  temp_vs_x_hist->Draw("COLZ");
 gPad->Update();
palette = (TPaletteAxis*)temp_vs_x_hist->GetListOfFunctions()->FindObject("palette");
palette->SetX1NDC(0.91);
 palette->SetX2NDC(0.93);
 palette->SetY1NDC(0.1);
 palette->SetY2NDC(0.9);
 palette->SetLabelSize(0.03);
 gStyle->SetTitleFontSize(0.07);
 gPad->Modified();
 gPad->Update();
  c1->SaveAs("Temp-vs-x.pdf");
  c1->Clear();
  temp_vs_y_hist->Draw("COLZ");
 gPad->Update();
palette = (TPaletteAxis*)temp_vs_y_hist->GetListOfFunctions()->FindObject("palette");
palette->SetX1NDC(0.91);
 palette->SetX2NDC(0.93);
 palette->SetY1NDC(0.1);
 palette->SetY2NDC(0.9);
 palette->SetLabelSize(0.03);
 gStyle->SetTitleFontSize(0.07);
 gPad->Modified();
 gPad->Update();
  c1->SaveAs("Temp-vs-y.pdf");
  c1->Clear();
  temp_vs_z_hist->Draw("COLZ");
 gPad->Update();
 palette = (TPaletteAxis*)temp_vs_z_hist->GetListOfFunctions()->FindObject("palette");
palette->SetX1NDC(0.91);
 palette->SetX2NDC(0.93);
 palette->SetY1NDC(0.1);
 palette->SetY2NDC(0.9);
 palette->SetLabelSize(0.03);
 gStyle->SetTitleFontSize(0.07);
 gPad->Modified();
 gPad->Update();
  c1->SaveAs("Temp-vs-z.pdf");

  std::unique_ptr<TFile> myFile( TFile::Open("Histos.root", "RECREATE") );
//  myFile->WriteObject(velocity_hist, "Velocity histogram");
  myFile->WriteObject(theta_hist, "Theta histogram");
  myFile->WriteObject(phi_hist, "Phi histogram");
//  myFile->WriteObject(r_energy_hist, "Recoil energy histogram");
//  myFile->WriteObject(phononNo_hist, "Primary phonon histogram");
//  myFile->WriteObject(xypos_hist, "Primary vertex position (X-Y)");
  myFile->WriteObject(vertex_hist, "Primary vertex position");
  myFile->WriteObject(initial_dir_hist, "Initial momentum direction");
//  myFile->WriteObject(zpos_hist, "Primary vertex position (X-Z)");
//  myFile->WriteObject(lfactor_hist, "Lindhard factor");
  myFile->WriteObject(TESxypos_hist, "Phonon hit position at TES");
  myFile->WriteObject(temperature_hist, "Temperature rise");
  myFile->WriteObject(temp_vs_x_hist, "Temperature vs primary x position");
  myFile->WriteObject(temp_vs_y_hist, "Temperature vs primary y position");
  myFile->WriteObject(temp_vs_z_hist, "Temperature vs primary z position");
//  myFile->WriteObject(edep_vs_Renergy, "Deposited vs recoil energy");

}

Double_t Get_temp(Double_t edep)
{
	Double_t HC_at_20mK, HC_at_1K=0.00104/184;	// In J/(g . K)
	Double_t volume=TMath::Pi()*2*2*2e-5, density=19;	// In cm^3 and g/cm^3
	
	HC_at_20mK=HC_at_1K*20*20*20e-9;

	return 1e+6*edep*1.6e-19/(HC_at_20mK*density*volume);
}*/
