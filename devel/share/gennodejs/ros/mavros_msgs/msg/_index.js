
"use strict";

let ESCTelemetryItem = require('./ESCTelemetryItem.js');
let HilControls = require('./HilControls.js');
let WaypointReached = require('./WaypointReached.js');
let HilGPS = require('./HilGPS.js');
let ExtendedState = require('./ExtendedState.js');
let State = require('./State.js');
let ADSBVehicle = require('./ADSBVehicle.js');
let WaypointList = require('./WaypointList.js');
let Trajectory = require('./Trajectory.js');
let CompanionProcessStatus = require('./CompanionProcessStatus.js');
let Mavlink = require('./Mavlink.js');
let RTKBaseline = require('./RTKBaseline.js');
let DebugValue = require('./DebugValue.js');
let CellularStatus = require('./CellularStatus.js');
let BatteryStatus = require('./BatteryStatus.js');
let VehicleInfo = require('./VehicleInfo.js');
let Tunnel = require('./Tunnel.js');
let OnboardComputerStatus = require('./OnboardComputerStatus.js');
let AttitudeTarget = require('./AttitudeTarget.js');
let GPSRTK = require('./GPSRTK.js');
let ManualControl = require('./ManualControl.js');
let HilActuatorControls = require('./HilActuatorControls.js');
let Param = require('./Param.js');
let GPSRAW = require('./GPSRAW.js');
let MagnetometerReporter = require('./MagnetometerReporter.js');
let PositionTarget = require('./PositionTarget.js');
let HomePosition = require('./HomePosition.js');
let GlobalPositionTarget = require('./GlobalPositionTarget.js');
let MountControl = require('./MountControl.js');
let HilStateQuaternion = require('./HilStateQuaternion.js');
let FileEntry = require('./FileEntry.js');
let Altitude = require('./Altitude.js');
let CameraImageCaptured = require('./CameraImageCaptured.js');
let ESCInfo = require('./ESCInfo.js');
let PlayTuneV2 = require('./PlayTuneV2.js');
let RadioStatus = require('./RadioStatus.js');
let TerrainReport = require('./TerrainReport.js');
let ESCStatusItem = require('./ESCStatusItem.js');
let EstimatorStatus = require('./EstimatorStatus.js');
let OverrideRCIn = require('./OverrideRCIn.js');
let ESCTelemetry = require('./ESCTelemetry.js');
let RCOut = require('./RCOut.js');
let LogData = require('./LogData.js');
let ActuatorControl = require('./ActuatorControl.js');
let OpticalFlowRad = require('./OpticalFlowRad.js');
let CamIMUStamp = require('./CamIMUStamp.js');
let LandingTarget = require('./LandingTarget.js');
let LogEntry = require('./LogEntry.js');
let NavControllerOutput = require('./NavControllerOutput.js');
let TimesyncStatus = require('./TimesyncStatus.js');
let Waypoint = require('./Waypoint.js');
let ParamValue = require('./ParamValue.js');
let GPSINPUT = require('./GPSINPUT.js');
let RTCM = require('./RTCM.js');
let Vibration = require('./Vibration.js');
let VFR_HUD = require('./VFR_HUD.js');
let SysStatus = require('./SysStatus.js');
let WheelOdomStamped = require('./WheelOdomStamped.js');
let StatusText = require('./StatusText.js');
let ESCInfoItem = require('./ESCInfoItem.js');
let ESCStatus = require('./ESCStatus.js');
let HilSensor = require('./HilSensor.js');
let CommandCode = require('./CommandCode.js');
let Thrust = require('./Thrust.js');
let RCIn = require('./RCIn.js');

module.exports = {
  ESCTelemetryItem: ESCTelemetryItem,
  HilControls: HilControls,
  WaypointReached: WaypointReached,
  HilGPS: HilGPS,
  ExtendedState: ExtendedState,
  State: State,
  ADSBVehicle: ADSBVehicle,
  WaypointList: WaypointList,
  Trajectory: Trajectory,
  CompanionProcessStatus: CompanionProcessStatus,
  Mavlink: Mavlink,
  RTKBaseline: RTKBaseline,
  DebugValue: DebugValue,
  CellularStatus: CellularStatus,
  BatteryStatus: BatteryStatus,
  VehicleInfo: VehicleInfo,
  Tunnel: Tunnel,
  OnboardComputerStatus: OnboardComputerStatus,
  AttitudeTarget: AttitudeTarget,
  GPSRTK: GPSRTK,
  ManualControl: ManualControl,
  HilActuatorControls: HilActuatorControls,
  Param: Param,
  GPSRAW: GPSRAW,
  MagnetometerReporter: MagnetometerReporter,
  PositionTarget: PositionTarget,
  HomePosition: HomePosition,
  GlobalPositionTarget: GlobalPositionTarget,
  MountControl: MountControl,
  HilStateQuaternion: HilStateQuaternion,
  FileEntry: FileEntry,
  Altitude: Altitude,
  CameraImageCaptured: CameraImageCaptured,
  ESCInfo: ESCInfo,
  PlayTuneV2: PlayTuneV2,
  RadioStatus: RadioStatus,
  TerrainReport: TerrainReport,
  ESCStatusItem: ESCStatusItem,
  EstimatorStatus: EstimatorStatus,
  OverrideRCIn: OverrideRCIn,
  ESCTelemetry: ESCTelemetry,
  RCOut: RCOut,
  LogData: LogData,
  ActuatorControl: ActuatorControl,
  OpticalFlowRad: OpticalFlowRad,
  CamIMUStamp: CamIMUStamp,
  LandingTarget: LandingTarget,
  LogEntry: LogEntry,
  NavControllerOutput: NavControllerOutput,
  TimesyncStatus: TimesyncStatus,
  Waypoint: Waypoint,
  ParamValue: ParamValue,
  GPSINPUT: GPSINPUT,
  RTCM: RTCM,
  Vibration: Vibration,
  VFR_HUD: VFR_HUD,
  SysStatus: SysStatus,
  WheelOdomStamped: WheelOdomStamped,
  StatusText: StatusText,
  ESCInfoItem: ESCInfoItem,
  ESCStatus: ESCStatus,
  HilSensor: HilSensor,
  CommandCode: CommandCode,
  Thrust: Thrust,
  RCIn: RCIn,
};
