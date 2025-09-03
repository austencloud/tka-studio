<script lang="ts">
  export let color: string;

  // Calculate styles based on the color prop
  const borderColor = color === "blue" ? "#2E3192" : "#ED1C24";
  const backgroundColor = color === "blue" ? "#e6f0ff" : "#ffe6e6";

  const boxStyles = `
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 2px dashed ${borderColor};
    background-color: ${backgroundColor};
    border-radius: 8px;
    padding: 20px;
    flex: 1;
    height: 100%;
  `;
</script>

<div style={boxStyles}>
  <p>Orientation Picker for {color === "blue" ? "Left" : "Right"}</p>
</div>
