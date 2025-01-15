// Auto-generated. Do not edit!

// (in-package imu_nav_ml.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class ImuNavPrediction {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.position = null;
      this.velocity = null;
      this.position_error_3d = null;
      this.velocity_error_3d = null;
      this.inference_time = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('position')) {
        this.position = initObj.position
      }
      else {
        this.position = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('velocity')) {
        this.velocity = initObj.velocity
      }
      else {
        this.velocity = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('position_error_3d')) {
        this.position_error_3d = initObj.position_error_3d
      }
      else {
        this.position_error_3d = 0.0;
      }
      if (initObj.hasOwnProperty('velocity_error_3d')) {
        this.velocity_error_3d = initObj.velocity_error_3d
      }
      else {
        this.velocity_error_3d = 0.0;
      }
      if (initObj.hasOwnProperty('inference_time')) {
        this.inference_time = initObj.inference_time
      }
      else {
        this.inference_time = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ImuNavPrediction
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [position]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.position, buffer, bufferOffset);
    // Serialize message field [velocity]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.velocity, buffer, bufferOffset);
    // Serialize message field [position_error_3d]
    bufferOffset = _serializer.float32(obj.position_error_3d, buffer, bufferOffset);
    // Serialize message field [velocity_error_3d]
    bufferOffset = _serializer.float32(obj.velocity_error_3d, buffer, bufferOffset);
    // Serialize message field [inference_time]
    bufferOffset = _serializer.float32(obj.inference_time, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ImuNavPrediction
    let len;
    let data = new ImuNavPrediction(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [position]
    data.position = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [velocity]
    data.velocity = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [position_error_3d]
    data.position_error_3d = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [velocity_error_3d]
    data.velocity_error_3d = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [inference_time]
    data.inference_time = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 60;
  }

  static datatype() {
    // Returns string type for a message object
    return 'imu_nav_ml/ImuNavPrediction';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2a3de14811f7c35ef90a6a889e58a171';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    geometry_msgs/Point position
    geometry_msgs/Vector3 velocity
    float32 position_error_3d
    float32 velocity_error_3d
    float32 inference_time
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ImuNavPrediction(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.position !== undefined) {
      resolved.position = geometry_msgs.msg.Point.Resolve(msg.position)
    }
    else {
      resolved.position = new geometry_msgs.msg.Point()
    }

    if (msg.velocity !== undefined) {
      resolved.velocity = geometry_msgs.msg.Vector3.Resolve(msg.velocity)
    }
    else {
      resolved.velocity = new geometry_msgs.msg.Vector3()
    }

    if (msg.position_error_3d !== undefined) {
      resolved.position_error_3d = msg.position_error_3d;
    }
    else {
      resolved.position_error_3d = 0.0
    }

    if (msg.velocity_error_3d !== undefined) {
      resolved.velocity_error_3d = msg.velocity_error_3d;
    }
    else {
      resolved.velocity_error_3d = 0.0
    }

    if (msg.inference_time !== undefined) {
      resolved.inference_time = msg.inference_time;
    }
    else {
      resolved.inference_time = 0.0
    }

    return resolved;
    }
};

module.exports = ImuNavPrediction;
