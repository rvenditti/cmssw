import FWCore.ParameterSet.Config as cms

### HLT filter
import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
ZMuHLTFilter = copy.deepcopy(hltHighLevel)
ZMuHLTFilter.throw = cms.bool(False)
ZMuHLTFilter.HLTPaths = ["HLT_Mu*","HLT_IsoMu*","HLT_DoubleMu*"]

### Z -> MuMu candidates

# Get muons of needed quality for Zs
looseMuonsForZMuSkim = cms.EDFilter("MuonSelector",
                             src = cms.InputTag("muons"),
                             cut = cms.string('pt > 5 &&  abs(eta)<2.4'),
                             filter = cms.bool(True)                                
                             )

tightMuonsForZMuSkim = cms.EDFilter("MuonSelector",
                             src = cms.InputTag("looseMuonsForZMuSkim"),
                             cut = cms.string('pt > 25 &&  abs(eta)<2.4 && isGlobalMuon = 1 && isTrackerMuon = 1 && abs(innerTrack().dxy)<2.0 && (globalTrack().normalizedChi2() < 10) && (innerTrack().hitPattern().numberOfValidHits() > 10) && (isolationR03().sumPt/pt)<0.4'),
                             filter = cms.bool(True)                                
                             )

# build Z-> MuMu candidates
dimuonsZMuSkim = cms.EDProducer("CandViewShallowCloneCombiner",
                         checkCharge = cms.bool(False),
                         cut = cms.string('mass > 60 && mass < 120 && charge=0'),
                         decay = cms.string("tightMuonsForZMuSkim looseMuonsForZMuSkim")
                         )



# Z filter
dimuonsFilterZMuSkim = cms.EDFilter("CandViewCountFilter",
                             src = cms.InputTag("dimuonsZMuSkim"),
                             minNumber = cms.uint32(1)
                             )



#InitialPlots = cms.EDAnalyzer('RecoMuonAnalyzer',
#                                   muonsInputTag = cms.InputTag("muons"),                                   )
#PlotsAfterTrigger = cms.EDAnalyzer('RecoMuonAnalyzer',
#                                   muonsInputTag = cms.InputTag("muons"),                                   )
#PlotsAfterLooseMuon = cms.EDAnalyzer('RecoMuonAnalyzer',
#                                   muonsInputTag = cms.InputTag("muons"),                                   )
#PlotsAfterTightMuon = cms.EDAnalyzer('RecoMuonAnalyzer',
#                                   muonsInputTag = cms.InputTag("muons"),
#                                   )
#PlotsAfterDiMuon = cms.EDAnalyzer('RecoMuonAnalyzer',
#                                   muonsInputTag = cms.InputTag("muons"),
#                                   )
#TFileService = cms.Service("TFileService",
#                                   fileName = cms.string("histoSingleMu_skim.root")#                                   )



# Z Skim sequence
diMuonSelSeq = cms.Sequence(
                            #InitialPlots *
                            ZMuHLTFilter *
                            #PlotsAfterTrigger *
                            looseMuonsForZMuSkim *
                            #PlotsAfterLooseMuon  *
                            tightMuonsForZMuSkim *
                            #PlotsAfterTightMuon *
                            dimuonsZMuSkim *
                            dimuonsFilterZMuSkim 
                            #PlotsAfterDiMuon
                            )
