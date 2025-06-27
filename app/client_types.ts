export type ClientSideContextInterface = {
  selectedImage: string;
};

export type ImageInterface = {
  name: string;
  url: string;
  id: number;
  width: number;
  height: number;
};

export const type ImageMetaData = {
  fileName: string,
  customName: string,
  uploadURL: string,
  id: number,
  width: number,
  height: number
}