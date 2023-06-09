export type Answer = string | string[];

export interface IWeek {
  wk_range: string;
  days: IDay[];
}

export interface IDay {
  num: number;
  focus: string;
  exs: IExs[] | null;
}

export interface IExs {
  name: string;
  type: string;
  sets: string | null;
  reps: string | null;
  dur: {
    val: number;
    unit: string;
  } | null;
}

export interface APIResponse {
  summary: string;
  num_wks: number;
  num_days: number;
  wks: IWeek[];
  notes: {
    content: string;
  }[];
}
