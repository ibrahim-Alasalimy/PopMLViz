import React, {Component} from "react";
import Select from "react-select";
import Collapse from "react-bootstrap/Collapse";
import {AiFillCaretDown} from "react-icons/ai";
import {Button, IconButton} from "@material-ui/core";
import OutlierBlock from "./OutlierBlock";
import Switch from "./Switch";
import {FcMindMap} from "react-icons/fc";
import {AiFillDelete} from "react-icons/ai";
import PropTypes from "prop-types";

class OutlierDetectionTab extends Component {
  state = {
    selectOutlierActions: [
      {
        label: "None",
        value: 0,
      },
      {
        label: "1 SD",
        value: 1,
      },
      {
        label: "2 SD",
        value: 2,
      },
      {
        label: "3 SD",
        value: 3,
      },
      {
        label: "Isolation Forest",
        value: 4,
      },
      {
        label: "Minimum Covariance Determinant",
        value: 5,
      },
      {
        label: "Local Outlier Factor",
        value: 6,
      },
      {
        label: "OneClassSVM",
        value: 7,
      },
    ],
    selectedOutlierMethod: {
      label: "None",
      value: 0,
    },
    open: false,
    columnRange: [1, this.props.numFeatures],
    pressed: false,
    columnName: "",
    allActions: [],
  };
  setOpen = (open) => {
    this.setState({open: open});
  };
  findName = (allActions) => {
    if (
      allActions.filter((elem) => {
        return Array.isArray(elem) || elem.label.includes("PC");
      }).length > 0
    ) {
      // if there is a column that includes tsne
      return "PC";
    } else if (
      allActions.filter((elem) => {
        return Array.isArray(elem) || elem.label.includes("TSNE");
      }).length > 0
    ) {
      // if there is a column that includes tsne
      return "TSNE";
    } else {
      return "Variable";
    }
  };
  componentDidMount = () => {
    this.setState({
      columnRange: [1, this.props.numFeatures],
      allActions: this.props.allActions,
      columnName: this.findName(this.props.allActions),
    });
  };
  componentDidUpdate = (prevProps) => {
    if (prevProps.numFeatures !== this.props.numFeatures) {
      this.setState({
        columnRange: [1, this.props.numFeatures],
        allActions: this.props.allActions,
        columnName: this.findName(this.props.allActions),
      });
    }
  };
  handleChangeSwitch = (e) => {
    const pressed = e.target.checked;
    this.setState({pressed});
  };

  handleOutlierColumnChange = (data) => {
    this.setState({columnRange: data.columnRange});
  };
  handleOutlierChange = (option) => {
    this.setState({selectedOutlierMethod: option.value});
  };

  runOutliers = () => {
    this.props.onChange(this.state);
  };
  render() {
    return (
      <div>
        <div
          style={{
            marginBottom: "5%",
            justifyContent: "space-between",
            display: "flex",
            flexDirection: "row",
          }}
          onClick={() => this.setOpen(!this.state.open)}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "row",
              width: "80%",
            }}
          >
            <FcMindMap size={30} style={{marginRight: "3%", opacity: 0.5}} />
            <label>Outlier Detection </label>
          </div>

          <AiFillCaretDown style={{marginTop: "3%"}} />
        </div>

        <Collapse in={this.state.open}>
          <div id="example-collapse-text">
            <div
              style={{
                display: "flex",
                flexDirection: "row",
              }}
            >
              <div
                style={{
                  width: "60%",
                }}
              >
                <Select
                  options={this.state.selectOutlierActions}
                  defaultValue={
                    this.state.selectOutlierActions.filter((x) => {
                      return x.value === this.state.selectedOutlierMethod;
                    })[0]
                  }
                  styles={{
                    option: (provided, state) => ({
                      ...provided,
                      color: "black",
                    }),
                  }}
                  onChange={this.handleOutlierChange}
                />
              </div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  width: "20%",
                  color: "white",
                }}
              >
                {this.state.selectedOutlierMethod < 4 && (
                  <Switch
                    labelRight={this.state.pressed === true ? "OR" : "AND"}
                    labelLeft={"Mode:"}
                    //   disabled={true}
                    onChange={this.handleChangeSwitch}
                  />
                )}
              </div>
            </div>
            <OutlierBlock
              columnRange={this.state.columnRange}
              onChange={this.handleOutlierColumnChange}
              numFeatures={this.props.numFeatures}
              columnName={this.state.columnName}
            />

            <div
              style={{
                display: "flex",
                flexDirection: "row",
                justifyContent: "space-around",
              }}
            >
              <Button
                variant="outlined"
                onClick={this.runOutliers}
                style={{
                  // marginTop: '10%',
                  color: "#ebeff7",
                  fontWeight: "bold",
                  backgroundColor:
                    this.state.selectedOutlierMethod == null
                      ? "grey"
                      : "#1891fb",
                  marginTop: "5%",
                }}
                disabled={this.state.selectedOutlierMethod == null}
              >
                Detect Outliers
              </Button>
              <IconButton
                variant="outlined"
                aria-label="delete"
                size="medium"
                style={{
                  color: "red",
                  backgroundColor: "transparent",
                  marginTop: 10,
                }}
                onClick={this.props.removeOutliers}
              >
                <AiFillDelete />
              </IconButton>
            </div>
          </div>
        </Collapse>
      </div>
    );
  }
}

OutlierDetectionTab.propTypes = {
  numFeatures: PropTypes.number,
  removeOutliers: PropTypes.func,
  allActions: PropTypes.array,
};

export default OutlierDetectionTab;
