import ClientParameterInterface from "../client_types";
export default function ParameterContainer({ clientParameters } : ClientParameterInterface) {
  return <div className="flex flex-col">{JSON.stringify(clientParameters, null, 2)}</div>;
}