export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json }
  | Json[]

export interface Database {
  public: {
    Tables: {
      plans: {
        Row: {
          created_at: string | null
          id: string
          response: Json | null
        }
        Insert: {
          created_at?: string | null
          id?: string
          response?: Json | null
        }
        Update: {
          created_at?: string | null
          id?: string
          response?: Json | null
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}
