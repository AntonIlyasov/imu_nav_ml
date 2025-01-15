// Auto-generated. Do not edit!

// (in-package imu_nav_ml.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class PythonList {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.row = null;
    }
    else {
      if (initObj.hasOwnProperty('row')) {
        this.row = initObj.row
      }
      else {
        this.row = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type PythonList
    // Serialize message field [row]
    bufferOffset = _arraySerializer.float64(obj.row, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type PythonList
    let len;
    let data = new PythonList(null);
    // Deserialize message field [row]
    data.row = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.row.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'imu_nav_ml/PythonList';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7f476b09ffe66a6e073b86346f9b64b0';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] row
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new PythonList(null);
    if (msg.row !== undefined) {
      resolved.row = msg.row;
    }
    else {
      resolved.row = []
    }

    return resolved;
    }
};

module.exports = PythonList;
