#include <TTree.h>
#include <TFile.h>
#include <TROOT.h>

#ifndef TH_DEFINE
#define TH_DEFINE

class TreeHandler{
public:
	//PUT ALL INPUT AND OUTPUT BRANCHES HERE
	TTree* OutputTree; 
	TTree* InputTree;
	TFile* OutputFile;
	int index = -1;
	int NumEntries;

	int Next(){
		index++;
		if (index > NumEntries) return -1;
		return index;
	}

	int LoadEvent(){
		if (InputTree == nullptr) return -1;
		InputTree->GetEvent(index);
		return 0;
	}

	void Fill(){
		OutputFile->cd();
		gROOT->cd();
		InputTree->GetEvent(index);
		OutputTree->Fill();
	}

	void Write(){
		OutputFile->cd();
		OutputFile->Write();
		OutputFile->Close();
	}


	TreeHandler(TString input_tree_name, TString input_file_name, TString output_tree_name, TString outfile_name) 
	{

		auto InputFile = TFile::Open(input_file_name);
		InputTree = (TTree*) InputFile->Get(input_tree_name);
	
		InputTree->SetBranchAddress("NumHits", &sim_numhits);
 		InputTree->SetBranchAddress("Hit_energy", &sim_hit_e);
 		InputTree->SetBranchAddress("Hit_time", &sim_hit_t);
 		InputTree->SetBranchAddress("Hit_detId", &sim_hit_detId);
 		InputTree->SetBranchAddress("Hit_particlePdgId", &sim_hit_particlePdgId);
 		InputTree->SetBranchAddress("Hit_G4TrackId", &sim_hit_G4TrackId);
 		InputTree->SetBranchAddress("Hit_G4ParentTrackId", &sim_hit_G4ParentTrackId);
 		InputTree->SetBranchAddress("Hit_x", &sim_hit_x);
 		InputTree->SetBranchAddress("Hit_y", &sim_hit_y);
 		InputTree->SetBranchAddress("Hit_z", &sim_hit_z);
 		InputTree->SetBranchAddress("Hit_particleEnergy", &sim_hit_particleEnergy);
 		InputTree->SetBranchAddress("Hit_particlePx", &sim_hit_px);
 		InputTree->SetBranchAddress("Hit_particlePy", &sim_hit_py);
		InputTree->SetBranchAddress("Hit_particlePz", &sim_hit_pz);
		InputTree->SetBranchAddress("Hit_weight", &sim_hit_weight);
 		InputTree->SetBranchAddress("NumGenParticles", &sim_NumGenParticles);
 		InputTree->SetBranchAddress("GenParticle_index", &sim_GenParticle_index);
 		InputTree->SetBranchAddress("GenParticle_G4index", &sim_GenParticle_G4index);
 		InputTree->SetBranchAddress("GenParticle_pdgid", &sim_GenParticle_pdgid);
 		InputTree->SetBranchAddress("GenParticle_status", &sim_GenParticle_status);
 		InputTree->SetBranchAddress("GenParticle_time", &sim_GenParticle_time);
 		InputTree->SetBranchAddress("GenParticle_x", &sim_GenParticle_x);
 		InputTree->SetBranchAddress("GenParticle_y", &sim_GenParticle_y);
 		InputTree->SetBranchAddress("GenParticle_z", &sim_GenParticle_z);
 		InputTree->SetBranchAddress("GenParticle_energy", &sim_GenParticle_energy);
 		InputTree->SetBranchAddress("GenParticle_px", &sim_GenParticle_px);
 		InputTree->SetBranchAddress("GenParticle_py", &sim_GenParticle_py);
 		InputTree->SetBranchAddress("GenParticle_pz", &sim_GenParticle_pz);
 		InputTree->SetBranchAddress("GenParticle_mo1", &sim_GenParticle_mo1);
 		InputTree->SetBranchAddress("GenParticle_mo2", &sim_GenParticle_mo2);
 		InputTree->SetBranchAddress("GenParticle_dau1", &sim_GenParticle_dau1);
 		InputTree->SetBranchAddress("GenParticle_dau2", &sim_GenParticle_dau2);
 		InputTree->SetBranchAddress("GenParticle_mass", &sim_GenParticle_mass);
 		InputTree->SetBranchAddress("GenParticle_pt", &sim_GenParticle_pt);
 		InputTree->SetBranchAddress("GenParticle_eta", &sim_GenParticle_eta);
 		InputTree->SetBranchAddress("GenParticle_phi", &sim_GenParticle_phi);
 		InputTree->SetBranchAddress("COSMIC_EVENT_ID", &sim_COSMIC_EVENT_ID);
 		InputTree->SetBranchAddress("COSMIC_CORE_X", &sim_COSMIC_CORE_X);
 		InputTree->SetBranchAddress("COSMIC_CORE_Y", &sim_COSMIC_CORE_Y);
 		InputTree->SetBranchAddress("COSMIC_GEN_PRIMARY_ENERGY", &sim_COSMIC_GEN_PRIMARY_ENERGY);
 		InputTree->SetBranchAddress("COSMIC_GEN_THETA", &sim_COSMIC_GEN_THETA);
 		InputTree->SetBranchAddress("COSMIC_GEN_PHI", &sim_COSMIC_GEN_PHI);
 		InputTree->SetBranchAddress("COSMIC_GEN_FIRST_HEIGHT", &sim_COSMIC_GEN_FIRST_HEIGHT);
 		InputTree->SetBranchAddress("COSMIC_GEN_ELECTRON_COUNT", &sim_COSMIC_GEN_ELECTRON_COUNT);
 		InputTree->SetBranchAddress("COSMIC_GEN_MUON_COUNT", &sim_COSMIC_GEN_MUON_COUNT);
 		InputTree->SetBranchAddress("COSMIC_GEN_HADRON_COUNT", &sim_COSMIC_GEN_HADRON_COUNT);
 		InputTree->SetBranchAddress("COSMIC_GEN_PRIMARY_ID", &sim_COSMIC_GEN_PRIMARY_ID);
 		InputTree->SetBranchAddress("EXTRA_11", &sim_EXTRA_11);
 		InputTree->SetBranchAddress("EXTRA_12", &sim_EXTRA_12);
 		InputTree->SetBranchAddress("EXTRA_13", &sim_EXTRA_13);
 		InputTree->SetBranchAddress("EXTRA_14", &sim_EXTRA_14);
 		InputTree->SetBranchAddress("EXTRA_15", &sim_EXTRA_15);

 		NumEntries = InputTree->GetEntries();
 		
 		OutputFile = new TFile(outfile_name, "RECREATE");
		OutputTree = new TTree(output_tree_name, "MATHUSLA Tree");

		OutputTree->Branch("NumHits", &sim_numhits);
		OutputTree->Branch("Hit_energy", "std::vector<double>", sim_hit_e);
 		OutputTree->Branch("Hit_time", "std::vector<double>", sim_hit_t);
 		OutputTree->Branch("Hit_detId", "std::vector<double>", sim_hit_detId);
 		OutputTree->Branch("Hit_particlePdgId", "std::vector<double>", sim_hit_particlePdgId);
 		OutputTree->Branch("Hit_G4TrackId", "std::vector<double>", sim_hit_G4TrackId);
 		OutputTree->Branch("Hit_G4ParentTrackId", "std::vector<double>", sim_hit_G4ParentTrackId);
 		OutputTree->Branch("Hit_x", "std::vector<double>", sim_hit_x);
 		OutputTree->Branch("Hit_y", "std::vector<double>", sim_hit_y);
 		OutputTree->Branch("Hit_z", "std::vector<double>", sim_hit_z);
 		OutputTree->Branch("Hit_particleEnergy", "std::vector<double>", sim_hit_particleEnergy);
 		OutputTree->Branch("Hit_particlePx", "std::vector<double>", sim_hit_px);
 		OutputTree->Branch("Hit_particlePy", "std::vector<double>", sim_hit_py);
		OutputTree->Branch("Hit_particlePz", "std::vector<double>", sim_hit_pz);
		OutputTree->Branch("Hit_weight", "std::vector<double>", sim_hit_weight);
 		OutputTree->Branch("NumGenParticles", &sim_NumGenParticles);
 		OutputTree->Branch("GenParticle_index", "std::vector<double>", sim_GenParticle_index);
 		OutputTree->Branch("GenParticle_G4index", "std::vector<double>", sim_GenParticle_G4index);
 		OutputTree->Branch("GenParticle_pdgid", "std::vector<double>", sim_GenParticle_pdgid);
 		OutputTree->Branch("GenParticle_status", "std::vector<double>", sim_GenParticle_status);
 		OutputTree->Branch("GenParticle_time", "std::vector<double>", sim_GenParticle_time);
 		OutputTree->Branch("GenParticle_x", "std::vector<double>", sim_GenParticle_x);
 		OutputTree->Branch("GenParticle_y", "std::vector<double>", sim_GenParticle_y);
 		OutputTree->Branch("GenParticle_z", "std::vector<double>", sim_GenParticle_z);
 		OutputTree->Branch("GenParticle_energy", "std::vector<double>", sim_GenParticle_energy);
 		OutputTree->Branch("GenParticle_px", "std::vector<double>", sim_GenParticle_px);
 		OutputTree->Branch("GenParticle_py", "std::vector<double>", sim_GenParticle_py);
 		OutputTree->Branch("GenParticle_pz", "std::vector<double>", sim_GenParticle_pz);
 		OutputTree->Branch("GenParticle_mo1", "std::vector<double>", sim_GenParticle_mo1);
 		OutputTree->Branch("GenParticle_mo2", "std::vector<double>", sim_GenParticle_mo2);
 		OutputTree->Branch("GenParticle_dau1", "std::vector<double>", sim_GenParticle_dau1);
 		OutputTree->Branch("GenParticle_dau2", "std::vector<double>", sim_GenParticle_dau2);
 		OutputTree->Branch("GenParticle_mass", "std::vector<double>", sim_GenParticle_mass);
 		OutputTree->Branch("GenParticle_pt", "std::vector<double>", sim_GenParticle_pt);
 		OutputTree->Branch("GenParticle_eta", "std::vector<double>", sim_GenParticle_eta);
 		OutputTree->Branch("GenParticle_phi", "std::vector<double>", sim_GenParticle_phi);
 		OutputTree->Branch("COSMIC_EVENT_ID", "std::vector<double>", sim_COSMIC_EVENT_ID);
 		OutputTree->Branch("COSMIC_CORE_X", "std::vector<double>", sim_COSMIC_CORE_X);
 		OutputTree->Branch("COSMIC_CORE_Y", "std::vector<double>", sim_COSMIC_CORE_Y);
 		OutputTree->Branch("COSMIC_GEN_PRIMARY_ENERGY", "std::vector<double>", sim_COSMIC_GEN_PRIMARY_ENERGY);
 		OutputTree->Branch("COSMIC_GEN_THETA", "std::vector<double>", sim_COSMIC_GEN_THETA);
 		OutputTree->Branch("COSMIC_GEN_PHI", "std::vector<double>", sim_COSMIC_GEN_PHI);
 		OutputTree->Branch("COSMIC_GEN_FIRST_HEIGHT", "std::vector<double>", sim_COSMIC_GEN_FIRST_HEIGHT);
 		OutputTree->Branch("COSMIC_GEN_ELECTRON_COUNT", "std::vector<double>", sim_COSMIC_GEN_ELECTRON_COUNT);
 		OutputTree->Branch("COSMIC_GEN_MUON_COUNT", "std::vector<double>", sim_COSMIC_GEN_MUON_COUNT);
 		OutputTree->Branch("COSMIC_GEN_HADRON_COUNT", "std::vector<double>", sim_COSMIC_GEN_HADRON_COUNT);
 		OutputTree->Branch("COSMIC_GEN_PRIMARY_ID", "std::vector<double>", sim_COSMIC_GEN_PRIMARY_ID);
 		OutputTree->Branch("EXTRA_11", "std::vector<double>", sim_EXTRA_11);
 		OutputTree->Branch("EXTRA_12", "std::vector<double>", sim_EXTRA_12);
 		OutputTree->Branch("EXTRA_13", "std::vector<double>", sim_EXTRA_13);
 		OutputTree->Branch("EXTRA_14", "std::vector<double>", sim_EXTRA_14);
 		OutputTree->Branch("EXTRA_15", "std::vector<double>", sim_EXTRA_15);

 		OutputTree->Branch("NumVertices", &numvertices, "NumVertices/D");
      	OutputTree->Branch("Vertex_numTracks", &vertex_numTracks);
      	OutputTree->Branch("Vertex_t", &vertex_t);
      	OutputTree->Branch("Vertex_x", &vertex_x);
      	OutputTree->Branch("Vertex_y", &vertex_y);
      	OutputTree->Branch("Vertex_z", &vertex_z);
      	OutputTree->Branch("Vertex_ErrorT", &vertex_t_error);
      	OutputTree->Branch("Vertex_ErrorX", &vertex_x_error);
      	OutputTree->Branch("Vertex_ErrorY", &vertex_y_error);
      	OutputTree->Branch("Vertex_ErrorZ", &vertex_z_error);
      	OutputTree->Branch("Vertex_chi2", &vertex_chi2);
      	OutputTree->Branch("Vertex_chi2PerNdof", &vertex_chi2_per_dof);
      	OutputTree->Branch("Vertex_chi2PValue", &vertex_chi2_p_value);

      	OutputTree->Branch("NumTracks", &numtracks, "NumTracks/D");
      	OutputTree->Branch("Track_numHits", &track_numHits);
      	OutputTree->Branch("Track_t0", &track_t);
      	OutputTree->Branch("Track_x0", &track_x);
      	OutputTree->Branch("Track_y0", &track_y);
      	OutputTree->Branch("Track_z0", &track_z);
      	OutputTree->Branch("Track_velX", &track_vx);
      	OutputTree->Branch("Track_velY", &track_vy);
      	OutputTree->Branch("Track_velZ", &track_vz);
      	OutputTree->Branch("Track_ErrorT0", &track_t_error);
      	OutputTree->Branch("Track_ErrorX0", &track_x_error);
      	OutputTree->Branch("Track_ErrorY0", &track_y_error);
      	OutputTree->Branch("Track_ErrorZ0", &track_z_error);
      	OutputTree->Branch("Track_ErrorVx", &track_vx_error);
      	OutputTree->Branch("Track_ErrorVy", &track_vy_error);
      	OutputTree->Branch("Track_ErrorVz", &track_vz_error);
      	OutputTree->Branch("Track_chi2", &track_chi2);
      	OutputTree->Branch("Track_chi2PerNdof", &track_chi2_per_dof);
      	OutputTree->Branch("Track_chi2PValue", &track_chi2_p_value);
      	OutputTree->Branch("Track_beta", &track_beta);
      	OutputTree->Branch("Track_ErrorBeta", &track_beta_error);
      	OutputTree->Branch("Track_angle", &track_angle);
     	OutputTree->Branch("Track_ErrorAngle", &track_angle_error);
     	OutputTree->Branch("Track_detCount", &unique_detector_count);
      	OutputTree->Branch("Track_expectedHitLayer", &track_expected_hit_layer);
      	OutputTree->Branch("Track_missingHitLayer", &track_missing_hit_layer);

      	OutputTree->Branch("Digi_numHits", &Digi_numHits, "Digi_numHits/D");
      	OutputTree->Branch("Digi_time", &digi_hit_t);
      	OutputTree->Branch("Digi_x", &digi_hit_x);
      	OutputTree->Branch("Digi_y", &digi_hit_y);
      	OutputTree->Branch("Digi_z", &digi_hit_z);
      	OutputTree->Branch("Digi_energy", &digi_hit_e);
      	OutputTree->Branch("Digi_px", &digi_hit_px);
      	OutputTree->Branch("Digi_py", &digi_hit_py);
      	OutputTree->Branch("Digi_pz", &digi_hit_pz);
      	OutputTree->Branch("Digi_hitIndices", &digi_hit_indices);


	}


  //____________________________________________________________________________________________

 //___Make Sim Branches_________________________________________________________________________
 	Double_t sim_numhits;
 	std::vector<double> *sim_hit_e = nullptr; 
 	std::vector<double> *sim_hit_t = nullptr; 
 	std::vector<double> *sim_hit_detId = nullptr; 
 	std::vector<double> *sim_hit_particlePdgId = nullptr;  
 	std::vector<double> *sim_hit_G4TrackId = nullptr; 
 	std::vector<double> *sim_hit_G4ParentTrackId = nullptr;  
 	std::vector<double> *sim_hit_x = nullptr;  
 	std::vector<double> *sim_hit_y = nullptr;  
 	std::vector<double> *sim_hit_z = nullptr;  
 	std::vector<double> *sim_hit_particleEnergy = nullptr; 
 	std::vector<double> *sim_hit_px = nullptr;  
 	std::vector<double> *sim_hit_py = nullptr;
 	std::vector<double> *sim_hit_pz = nullptr;  
 	std::vector<double> *sim_hit_weight = nullptr; 
 	Double_t sim_NumGenParticles;
 	std::vector<double> *sim_GenParticle_index = nullptr;  
 	std::vector<double> *sim_GenParticle_G4index = nullptr; 
 	std::vector<double> *sim_GenParticle_pdgid = nullptr;  
 	std::vector<double> *sim_GenParticle_status = nullptr;  
 	std::vector<double> *sim_GenParticle_time = nullptr; 
 	std::vector<double> *sim_GenParticle_x = nullptr;  
 	std::vector<double> *sim_GenParticle_y = nullptr;  
 	std::vector<double> *sim_GenParticle_z = nullptr; 
 	std::vector<double> *sim_GenParticle_energy = nullptr;
 	std::vector<double> *sim_GenParticle_px = nullptr;  
 	std::vector<double> *sim_GenParticle_py = nullptr; 
 	std::vector<double> *sim_GenParticle_pz = nullptr;  
 	std::vector<double> *sim_GenParticle_mo1 = nullptr; 
 	std::vector<double> *sim_GenParticle_mo2 = nullptr; 
 	std::vector<double> *sim_GenParticle_dau1 = nullptr;  
 	std::vector<double> *sim_GenParticle_dau2 = nullptr;  
 	std::vector<double> *sim_GenParticle_mass = nullptr; 
 	std::vector<double> *sim_GenParticle_pt = nullptr;  
 	std::vector<double> *sim_GenParticle_eta = nullptr; 
 	std::vector<double> *sim_GenParticle_phi = nullptr;  
 	std::vector<double> *sim_COSMIC_EVENT_ID = nullptr;  
 	std::vector<double> *sim_COSMIC_CORE_X = nullptr; 
 	std::vector<double> *sim_COSMIC_CORE_Y = nullptr;  
 	std::vector<double> *sim_COSMIC_GEN_PRIMARY_ENERGY = nullptr;  
 	std::vector<double> *sim_COSMIC_GEN_THETA = nullptr;  
 	std::vector<double> *sim_COSMIC_GEN_PHI = nullptr;  
 	std::vector<double> *sim_COSMIC_GEN_FIRST_HEIGHT = nullptr;
 	std::vector<double> *sim_COSMIC_GEN_ELECTRON_COUNT = nullptr;
 	std::vector<double> *sim_COSMIC_GEN_MUON_COUNT = nullptr; 
 	std::vector<double> *sim_COSMIC_GEN_HADRON_COUNT = nullptr;  
 	std::vector<double> *sim_COSMIC_GEN_PRIMARY_ID = nullptr;
 	std::vector<double> *sim_EXTRA_11 = nullptr; 
 	std::vector<double> *sim_EXTRA_12 = nullptr;
 	std::vector<double> *sim_EXTRA_13 = nullptr;
 	std::vector<double> *sim_EXTRA_14 = nullptr;
 	std::vector<double> *sim_EXTRA_15 = nullptr;

 		//__Make Vertex Branches________________________________________________________________________
  	std::vector<double> vertex_numTracks;
  	std::vector<double> vertex_chi2;
  	std::vector<double> vertex_chi2_per_dof;
 	std::vector<double> vertex_chi2_p_value;
  	std::vector<double> vertex_t;
  	std::vector<double> vertex_x;
  	std::vector<double> vertex_y;
  	std::vector<double> vertex_z;
  	std::vector<double> vertex_t_error;
  	std::vector<double> vertex_x_error;
  	std::vector<double> vertex_y_error;
  	std::vector<double> vertex_z_error;
  	Double_t numvertices;



  //__Make Track Branches_________________________________________________________________________
  	std::vector<double> track_numHits;
  	std::vector<double> track_chi2;
  	std::vector<double> track_chi2_per_dof;
  	std::vector<double> track_chi2_p_value;
  	std::vector<double> track_beta;
  	std::vector<double> track_beta_error;
  	std::vector<double> track_angle;
  	std::vector<double> track_angle_error;
  	std::vector<double> unique_detector_count;
  	std::vector<double> track_t;
  	std::vector<double> track_x;
  	std::vector<double> track_y;
  	std::vector<double> track_z;
  	std::vector<double> track_vx;
  	std::vector<double> track_vy;
  	std::vector<double> track_vz;
  	std::vector<double> track_t_error;
  	std::vector<double> track_x_error;
  	std::vector<double> track_y_error;
  	std::vector<double> track_z_error;
  	std::vector<double> track_vx_error;
  	std::vector<double> track_vy_error;
  	std::vector<double> track_vz_error;
  	std::vector<int>track_expected_hit_layer;
  	std::vector<int> track_missing_hit_layer;
  	Double_t numtracks;

  
  //___Make Digi Branches_____________________________________________________________________
  	std::vector<double> digi_hit_t;
  	std::vector<double> digi_hit_x;
  	std::vector<double> digi_hit_y;
  	std::vector<double> digi_hit_z;
  	std::vector<double> digi_hit_e;
  	std::vector<double> digi_hit_px;
  	std::vector<double> digi_hit_py;
  	std::vector<double> digi_hit_pz;
  	std::vector<int> digi_hit_indices;
  	Double_t Digi_numHits;





}; //class TreeHandler





#endif