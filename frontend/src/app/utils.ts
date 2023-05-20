interface dataProps {
  answer: Record<number, string | string[]>;
}

const API_URL = "https://fitai-backend.onrender.com";
// const API_URL = "http://localhost:5000";

export const getWorkoutPlan = async (
  data: dataProps,
  endpoint: string = "/generate/"
) => {
  console.log("Fetching data");
  console.log("DATA: ", JSON.stringify(data));
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  const json = await response.json();
  console.log(json);
  return json;
};
