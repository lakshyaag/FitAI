interface dataProps {
  answer: {
    "1": string;
    "2": string;
    "3": number;
    "4": number;
    "5": string;
    "6": string;
    "7": string;
    "8": string;
    "9": string;
    "10": string;
    "11": string;
    "12": string;
    "13": string;
    "14": string;
    "15": string;
    "16": string[];
    "17": string;
    "18": string;
  };
}

const API_URL = 'https://fitai-backend.onrender.com/generate/'

export const getWorkoutPlan = async (data: dataProps) => {
  console.log('Fetching data')
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    const json = await response.json()
    console.log(json)
    return json
};
