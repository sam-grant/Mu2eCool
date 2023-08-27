{
	TFile *fin = TFile::Open("../ntuples/v3.06/g4beamline_ZNtupleDebug_5events.root");
	TTree *tree = (TTree*)fin->Get("NTuple/Z500");
	tree->Scan();
	fin->Close();
}