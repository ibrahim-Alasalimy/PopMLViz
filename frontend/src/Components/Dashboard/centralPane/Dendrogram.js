import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import "../dashboard.css"

const Dendrogram = ({ dendrogramPath }) => {
  const [image, setImage] = useState("");

  useEffect(() => {
    setImage(dendrogramPath);
  }, [dendrogramPath]);

  return (
    <div>
      {image !== "" && (
        <img
          src={`${process.env.REACT_APP_PROTOCOL}://${process.env.REACT_APP_DOMAIN}${process.env.REACT_APP_PORT}/api/dendrogram/${image}`}
          style={styles.image}
          className="scatter-plot"
          alt=""
        />
      )}
    </div>
  );
};

const styles = {
  image: {
    width: "100%",
    // position: "fixed",
    // zIndex: 1,
    // top: 0,
    // overflowX: "hidden",
    // left: 0,
    // marginTop: "13%",
    // marginLeft: "23%",
    // width: "55%",
    // height: "72%",
  },
};

Dendrogram.propTypes = {
  dendrogramPath: PropTypes.string,
};

export default Dendrogram;
