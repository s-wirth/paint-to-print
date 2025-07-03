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

export type ClientParameterInterface = {
  contourBox: {
    topLeft: {
      x: number | null;
      y: number | null;
    };
    topRight: {
      x: number | null;
      y: number | null;
    };
    bottomLeft: {
      x: number | null;
      y: number | null;
    };
    bottomRight: {
      x: number | null;
      y: number | null;
    };
  };
};