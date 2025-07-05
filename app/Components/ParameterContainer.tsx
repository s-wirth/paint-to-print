import ClientParameterInterface from "../client_types";
export default function ParameterContainer({ clientParameters, bbSelectionActive, setBBSelectionActive } : { clientParameters: ClientParameterInterface, bbSelectionActive: boolean, setBBSelectionActive: any }) {
  return <div className="flex flex-col">
    <button onClick={() => setBBSelectionActive(!bbSelectionActive)}>Define Painting Bounds</button>
    {JSON.stringify(clientParameters, null, 2)}
  </div>;
}