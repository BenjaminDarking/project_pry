import React, { Component } from "react";
import NeoVis from 'neovis.js';
const axios = require('axios');

export class Neo extends Component {
  state = {
    neo_labels: [],
    neo_relationships: []
  }



  fetchData() {
    let configs = {
      "Access-Control-Allow-Origin": "*"
    }

    axios.get('http://localhost:5000/', configs).then(response => {
      console.log(response.data)
      this.setState({
        neo_labels: response.data.label,
        neo_realtionships: response.data.relationships,
      })
      console.log(this.state.neo_labels)
      console.log(this.state.neo_relationships)
      let config = {
        container_id: "viz",
        labels: this.state.neo_labels,
        relationships: this.state.neo_realtionships,
        initial_cypher: "MATCH (p) RETURN p"
      };
      console.log(config.labels)
      console.log(config.relationships)

      var viz = new NeoVis(config);
      viz.render();
    })
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    return (
      <div>
        <div id="viz"></div>
      </div>
    );
  }
}

export default Neo;