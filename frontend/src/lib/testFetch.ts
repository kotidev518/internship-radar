export const testFetchAction = async () => {
    try {
        console.log("Initiating fetch...");
        const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetched data successfully:", data);
        alert(`Fetched successfully!\nTitle: ${data.title}`);
        return data;
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Fetch failed!");
        throw error;
    }
};
