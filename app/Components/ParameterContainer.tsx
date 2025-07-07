import ClientParameterInterface from "../client_types";
export default function ParameterContainer({ clientParameters, bbSelectionActive, setBBSelectionActive, submitBoundingRectPointsToMeta } : { clientParameters: ClientParameterInterface, bbSelectionActive: boolean, setBBSelectionActive: any }) {
  const boundsSelected = clientParameters.contourBox.p1.x !== null && clientParameters.contourBox.p2.x !== null && clientParameters.contourBox.p3.x !== null && clientParameters.contourBox.p4.x !== null;
  return <div className="flex flex-col">
    <button onClick={() => setBBSelectionActive(!bbSelectionActive)}>Define Painting Bounds</button>
    <button disabled={!boundsSelected} onClick={submitBoundingRectPointsToMeta}>Submit Painting Bounds</button>
    {JSON.stringify(clientParameters, null, 2)}
  </div>;
}