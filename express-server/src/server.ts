import app from "./app";
import { PORT } from "./utils/env";

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
