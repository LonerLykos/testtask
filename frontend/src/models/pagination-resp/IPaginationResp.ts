import {IProfile} from "../profile/IProfile.ts";

export interface IPaginationResp {
  total_items: number;
  total_pages: number;
  prev: boolean;
  next: boolean;
  data: IProfile[];
}