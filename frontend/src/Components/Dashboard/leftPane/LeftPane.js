import React from "react";
import { Button } from "@material-ui/core";
import UploadAndVisualizeTab from "./UploadAndVisualizeTab";
import ClusteringAlgorithmsTab from "./ClusteringAlgorithmsTab";
import OutlierDetectionTab from "./OutlierDetectionTab";
import colors from "../../../config/colors";
import { useNavigate } from "react-router-dom";


const LeftPane = ({
  UploadTabChange,
  samplePCAAdmixDataset2,
  handleProcessedPCA,
  handleProcessedAdmix,
  handleUnprocessedPCA,
  handleTSNE2D,
  handleTSNE3D,
  runPCAir,
  runCluster,
  runOutliers,
  allActions,
  removeOutliers,
  onPressReset,
  styles
}) => {

  const navigate = useNavigate();

  function handleHomeClick() {
    navigate("/");
  }
  return (
    <div className="leftpane" style={styles.leftPane}>
       <div onClick={handleHomeClick} style={{display: "flex", flexDirection: "row", marginTop: "5px", marginBottom: "50px", alignItems: 'center', cursor: "pointer"}}>
          <img src='../../../logo.jpeg'style={{ height:"40px",marginRight: "10px"}}/>
          <span style={{fontSize: "18px"}} >PopMLVis</span>
        </div>
      <form style={{ marginTop: "1%" }}>
        <UploadAndVisualizeTab
          onChange={UploadTabChange}
          samplePCAAdmixDataset={samplePCAAdmixDataset2}
          processedPCA={handleProcessedPCA} // handleFileUpload
          processedAdmix={handleProcessedAdmix} // handleAdmixFileUpload1
          unprocessedPCA={handleUnprocessedPCA}
          tsne2d={handleTSNE2D}
          tsne3d={handleTSNE3D}
          runPCAir={runPCAir}
        />
      </form>
      <hr style={{ backgroundColor: "white", height: 2, opacity: 1 }} />
      <ClusteringAlgorithmsTab onChange={runCluster} />
      <hr style={{ backgroundColor: "white", height: 2, opacity: 1 }} />
      <OutlierDetectionTab
        onChange={runOutliers}
        numFeatures={
          allActions.filter((elem) => {
            return Array.isArray(elem) || elem.label.includes("PC") || elem.label.includes("TSNE");
          }).length
        }
        allActions={allActions}
        removeOutliers={removeOutliers}
      />
      <div style={{ marginTop: "20%" }}>
        <Button
          variant="outlined"
          style={{
            color: "red",
            fontWeight: "bold",
            fontStyle: "italic",
            backgroundColor: "#ebeff7",
            marginLeft: "32%",
          }}
          onClick={onPressReset}
        >
          RESET
        </Button>
        {/* <div style={{height: 1000}}></div> */}
      </div>
    </div>
  );
};

export default LeftPane;
