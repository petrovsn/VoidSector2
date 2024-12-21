import React from 'react'
import { MeshObject } from "./graphics_core";


export class MarkerAsteroid extends React.Component {
  render() {
    const texture = 'asteroids/1.png'
    return (
      <MeshObject
        level={0}
        texture={texture}
        position={this.props.position}
        size={this.props.radius * 2}
        scale_factor={this.props.scale_factor}
        offset_factor={this.props.offset_factor}
      />
    )
  }
}


export class MarkerShip extends React.Component {
  render() {
    const texture = 'markers/ship.png'
    return (
      <MeshObject
        level={0}
        texture={texture}
        position={this.props.position}
        size={30}
        scale_factor={this.props.scale_factor}
        offset_factor={this.props.offset_factor}
      />
    )
  }
}


export class MarkerDot extends React.Component {
  render() {
    const texture = 'markers/dot.png'
    return (
      <MeshObject
        texture={texture}
        position={this.props.position}
        size={2}
        no_scale_size={true}
        level={this.props.level}
        color={this.props.color}
        scale_factor={this.props.scale_factor}
        scale_offset={this.props.scale_offset}
      />
    )
  }
}

//Гравитационные колодцы, радиусы досягаемости, etc
export class MarkerCircle extends React.Component {
  render() {
    let texture = 'markers/circle_normal.png'
    if (this.props.radius > 100) texture = 'markers/circle_thin.png'
    if (this.props.radius < 50) texture = 'markers/circle_bold.png'
    return (
      <MeshObject
        texture={texture}
        level={this.props.level}
        color={this.props.color}
        position={[this.props.position[0], this.props.position[1], 0]}
        size={this.props.radius * 2}
        scale_factor={this.props.scale_factor}
        scale_offset={this.props.scale_offset}
      />
    )
  }
}

export class MarkerDirection extends React.Component {
  render() {
    const texture = 'markers/direction.png'
    return (
      <MeshObject
        texture={texture}
        position={[this.props.position[0], this.props.position[1], 0]}
        size={50}
        rotation={this.props.rotation}
        color={this.props.color}
        scale_factor={this.props.scale_factor}
        scale_offset={this.props.scale_offset}
      />
    )
  }
}
