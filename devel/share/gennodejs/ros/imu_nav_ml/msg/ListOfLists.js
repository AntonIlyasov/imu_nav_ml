// Auto-generated. Do not edit!

// (in-package imu_nav_ml.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let PythonList = require('./PythonList.js');

//-----------------------------------------------------------

class ListOfLists {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.matrix = null;
    }
    else {
      if (initObj.hasOwnProperty('matrix')) {
        this.matrix = initObj.matrix
      }
      else {
        this.matrix = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ListOfLists
    // Serialize message field [matrix]
    // Serialize the length for message field [matrix]
    bufferOffset = _serializer.uint32(obj.matrix.length, buffer, bufferOffset);
    obj.matrix.forEach((val) => {
      bufferOffset = PythonList.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ListOfLists
    let len;
    let data = new ListOfLists(null);
    // Deserialize message field [matrix]
    // Deserialize array length for message field [matrix]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.matrix = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.matrix[i] = PythonList.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.matrix.forEach((val) => {
      length += PythonList.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'imu_nav_ml/ListOfLists';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fae0d37fb284617a626d94525abd3508';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    PythonList[] matrix
    
    ================================================================================
    MSG: imu_nav_ml/PythonList
    float64[] row
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ListOfLists(null);
    if (msg.matrix !== undefined) {
      resolved.matrix = new Array(msg.matrix.length);
      for (let i = 0; i < resolved.matrix.length; ++i) {
        resolved.matrix[i] = PythonList.Resolve(msg.matrix[i]);
      }
    }
    else {
      resolved.matrix = []
    }

    return resolved;
    }
};

module.exports = ListOfLists;
