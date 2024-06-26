import React, {Component} from "react";
import PropTypes from "prop-types";
import {Button} from "@material-ui/core";
import Select from "react-select";
import {CirclePicker} from "react-color";

class TabOutputOptions extends Component {
  state = {
    cluster_names: {},
    plotTitle: "",
    selectActions: [
      {value: "png", label: "png"},
      {value: "svg", label: "svg"},
      {value: "jpeg", label: "jpeg"},
      {value: "webp", label: "webp"},
    ],
    selectedColumn: "png",
    width: 800,
    height: 600,
    image: "",
    markerSize: 4,
    chosenInitialColor: "#f44336",
    selectShapeOptions: [
      {value: "circle", label: "circle"},
      {value: "square", label: "square"},
      {value: "diamond", label: "diamond"},
      {value: "x", label: "x"},
      {value: "star", label: "star"},
      {value: "triangle-up", label: "triangle-up"},
      {value: "bowtie", label: "bowtie"},
      {value: "pentagon", label: "pentagon"},
      {value: "hexagon", label: "hexagon"},
      {value: "star-diamond", label: "star-diamond"},
      {value: "circle-cross", label: "circle-cross"},
      {value: "hash", label: "hash"},
      {value: "y-up", label: "y-up"},
      {value: "line-ew", label: "line-ew"},
      {value: "arrow-down", label: "arrow-down"},
    ],

    selectedInitialShape: {value: "circle", label: "circle"},


  };
  handleFormatChange = (value) => {
    this.setState({
      selectedColumn: value.label,
    });
  };

  handleSelectShapeOptions = (value) => {
    this.setState({
      selectedInitialShape: value,
    });
  };
  componentDidMount = () => {
    this.setState({
      image: this.props.dendrogramPath,
      markerSize:
        this.props.markerSize !== undefined ? Number(this.props.markerSize) : 4,
    });
  };
  componentDidUpdate = (prevProps) => {
    if (prevProps.dendrogramPath !== this.props.dendrogramPath) {
      this.setState({
        image: this.props.dendrogramPath,
      });
    }
  };
  handleIncrementChange = (event) => {
    if (Number(event.target.value) >= 2 && event.target.value !== undefined) {
      this.setState({markerSize: Number(event.target.value)});
    }
  };
  showOutputOptions = () => {
    var num_clusters = this.props.uniqueClusters;
    if (num_clusters < 2) {
      num_clusters = 2;
    }
    return (
      <div style={{padding: "4%"}}>
        <div style={{display: "flex", flexDirection: "row"}}>
          <h6 style={{paddingTop: "2%", marginBottom: "10%"}}>
            Marker size:
          </h6>
          <div style={{width: "50%"}}>
            <input
              type="number"
              name="clicks"
              style={{width: "40%", marginLeft: "10%"}}
              value={Number(this.state.markerSize).toString()}
              onChange={this.handleIncrementChange}
            />
          </div>
        </div>

        <div style={{display: "flex", flexDirection: "row"}}>
          <h6 style={{paddingTop: "2%", marginBottom: "10%"}}>
            Marker Color:
          </h6>

          <div style={{width: "50%", paddingBottom: "10%", paddingLeft: "2%"}}>
            <CirclePicker circleSize={20} onChangeComplete={(color) => {console.log(color); this.setState({chosenInitialColor: color.hex})}} />
          </div>
        </div>

        <div style={{display: "flex", flexDirection: "row"}}>
          <h6 style={{paddingTop: "2%", marginBottom: "10%"}}>
            Marker Shape:
          </h6>

          <div style={{width: "50%", paddingBottom: "10%", paddingLeft: "2%"}}>
            <Select
              options={this.state.selectShapeOptions}
              onChange={this.handleSelectShapeOptions}
              defaultValue={this.state.selectedInitialShape}
            />
          </div>
        </div>

        <h6>Change plot title:</h6>
        <div
          style={{
            marginTop: "10px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div>
            <label style={{width: "30%"}}>Plot Title</label>
            <input
              type="text"
              style={{marginLeft: "5%", width: "60%"}}
              onChange={(e) => {
                this.setState({plotTitle: e.target.value});
              }}
            />
          </div>
          <div style={{marginTop: "2%"}}>
            <label style={{width: "30%"}}>Width</label>
            <input
              type="text"
              style={{marginLeft: "5%", width: "20%"}}
              defaultValue={this.state.width}
              onChange={(e) => {
                this.setState({width: e.target.value});
              }}
            />
          </div>
          <div style={{marginTop: "2%"}}>
            <label style={{width: "30%"}}>Height</label>
            <input
              type="text"
              defaultValue={this.state.height}
              style={{marginLeft: "5%", width: "20%"}}
              onChange={(e) => {
                this.setState({height: e.target.value});
              }}
            />
          </div>
          <div
            style={{marginTop: "2%", display: "flex", flexDirection: "row"}}
          >
            <label style={{width: "30%"}}>Format</label>
            <div style={{width: "50%", marginLeft: "5%"}}>
              <Select
                options={this.state.selectActions}
                onChange={this.handleFormatChange}
                defaultValue={this.state.selectedColumn}
              />
            </div>
          </div>
        </div>
        {this.props.showClusters && (
          <div>
            <h6 style={{marginTop: "10%"}}>Change cluster names:</h6>
            {[...Array(num_clusters)].map((_, index) => {
              return (
                <div style={{marginTop: "10px"}}>
                  <label style={{width: "30%"}}>Cluster {index}</label>
                  <input
                    type="text"
                    name={index}
                    style={{marginLeft: "5%", width: "60%"}}
                    onChange={(e) => {
                      var new_cluster_names = this.state.cluster_names;
                      new_cluster_names[index] = e.target.value;
                      this.setState({cluster_names: new_cluster_names});
                    }}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  };
  render() {
    return (
      <div>
        {this.showOutputOptions()}
        <Button
          variant="outlined"
          onClick={(event) => {
            this.props.parentCallback(this.state);
            event.preventDefault();
          }}
          style={{
            marginLeft: "50%",
            marginTop: "10%",
          }}
        >
          Submit
        </Button>
      </div>
    );
  }
}

TabOutputOptions.propTypes = {
  uniqueClusters: PropTypes.number,
  showClusters: PropTypes.bool,
  markerSize: PropTypes.number,
};

export default TabOutputOptions;
