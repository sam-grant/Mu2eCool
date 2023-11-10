void RecursiveVisible(TGeoVolume* vol)
{
  // if(!strstr(vol->GetName(), "CRS") && !strstr(vol->GetName(), "CMB") && !strstr(vol->GetName(), "CRV"))
  //   vol->SetVisibility(false);

  // if(!strstr(vol->GetName(), "Foil"))
  //    vol->SetVisibility(false);

  if(strstr(vol->GetName(), "Vacuum")){
    std::cout <<vol->GetName() << std::endl;
    vol->SetVisContainers(1);
    vol->SetFillColor(2);
    vol->SetVisibility(true);
  }
    
  // vol->SetVisContainers(1);
  
  // if(!strstr(vol->GetName(), "protonabs") && !strstr(vol->GetName(), "TSdA4") && !strstr(vol->GetName(), "TTrack")  && !strstr(vol->GetName(), "Foil"))
  //   vol->SetVisibility(false);

  // vol->SetLineColor(2);
  // vol->SetFillColor(2);
  // vol->SetVisibility(true);

  // if(!strstr(vol->GetName(), "protonabs1"))
  //   vol->SetVisibility(false);

  
  Int_t n_daughters = vol->GetNdaughters();
  for (Int_t i=0; i<n_daughters; i++) {
    RecursiveVisible(vol->GetNode(i)->GetVolume());
  }
}

void DrawGeom(const std::string& gdmlfile="../g4files/mu2e012323.gdml")
{
  TGeoManager *geom = TGeoManager::Import(gdmlfile.c_str());
  geom->SetVisLevel(4);
  geom->SetMaxVisNodes(1000000);
  
  // geom->SetVisOption(0);
  RecursiveVisible(geom->GetVolume("World"));  
  geom->GetVolume("World")->Draw("ogl");
  
}
