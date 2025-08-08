<!--
Simple Pictograph Test - Using Arrow Location Calculator
-->
<script lang="ts">
	import { ModernPictograph } from '$lib/components/pictograph';
	import { createPictographData } from '$lib/domain';

	// CSV data: A,alpha1,alpha3,split,same,pro,cw,s,w,pro,cw,n,e
	// This means:
	// - Blue: start=s, end=w, pro, clockwise → location should be 'sw' 
	// - Red: start=n, end=e, pro, clockwise → location should be 'ne'
	const correctPictographA = createPictographData({
		letter: 'A',
		grid_data: { mode: 'diamond' },
		arrows: {
			blue: {
				id: 'blue-arrow',
				arrow_type: 'blue',
				color: '#2E3192',
				motion_type: 'pro',
				location: 'sw',      // Calculated by ArrowLocationCalculator: start=s, end=w → sw
				start_orientation: 'in',
				end_orientation: 'out',
				rotation_direction: 'clockwise',
				turns: 0,
				is_mirrored: false,
				coordinates: null,
				rotation_angle: 180, // Need to look up correct rotation for SW + clockwise
				svg_center: null,
				svg_mirrored: false,
				metadata: {
					start_loc: 's',
					end_loc: 'w',
					calculated_location: 'sw'
				}
			},
			red: {
				id: 'red-arrow',
				arrow_type: 'red',
				color: '#ED1C24',
				motion_type: 'pro',
				location: 'ne',      // Calculated by ArrowLocationCalculator: start=n, end=e → ne
				start_orientation: 'in',
				end_orientation: 'out',
				rotation_direction: 'clockwise',
				turns: 0,
				is_mirrored: false,
				coordinates: null,
				rotation_angle: 0,   // Need to look up correct rotation for NE + clockwise
				svg_center: null,
				svg_mirrored: false,
				metadata: {
					start_loc: 'n',
					end_loc: 'e',
					calculated_location: 'ne'
				}
			}
		},
		props: {
			blue: {
				id: 'blue-staff',
				prop_type: 'staff',
				color: '#2E3192',
				location: 's',       // Props go at start location
				coordinates: null,
				rotation_angle: 0,
				svg_center: null,
				metadata: {
					orientation: 'in'
				}
			},
			red: {
				id: 'red-staff',
				prop_type: 'staff',
				color: '#ED1C24',
				location: 'n',       // Props go at start location
				coordinates: null,
				rotation_angle: 0,
				svg_center: null,
				metadata: {
					orientation: 'in'
				}
			}
		}
	});
</script>

<svelte:head>
	<title>Pictograph A Test - Arrow Location Calculator</title>
</svelte:head>

<main>
	<h1>Pictograph A Test - Arrow Location Calculator</h1>
	
	<div class="pictograph-container">
		<ModernPictograph 
			pictographData={correctPictographA}
			width={400}
			height={400}
		/>
	</div>
	
	<div class="explanation">
		<h2>Arrow Location Logic</h2>
		<p><strong>CSV:</strong> <code>A,alpha1,alpha3,split,same,pro,cw,s,w,pro,cw,n,e</code></p>
		
		<div class="location-calcs">
			<div class="calc blue-calc">
				<h3>Blue Arrow Calculation</h3>
				<p>• Start: <strong>s</strong> (south)</p>
				<p>• End: <strong>w</strong> (west)</p>
				<p>• Motion: <strong>pro</strong> (clockwise)</p>
				<p>• <strong>Location Calculator:</strong> s + w = <strong>sw</strong> (southwest)</p>
				<p>• Arrow should render at <strong>southwest</strong> position</p>
				<p>• Staff should be at <strong>south</strong> (start position)</p>
			</div>
			
			<div class="calc red-calc">
				<h3>Red Arrow Calculation</h3>
				<p>• Start: <strong>n</strong> (north)</p>
				<p>• End: <strong>e</strong> (east)</p>
				<p>• Motion: <strong>pro</strong> (clockwise)</p>
				<p>• <strong>Location Calculator:</strong> n + e = <strong>ne</strong> (northeast)</p>
				<p>• Arrow should render at <strong>northeast</strong> position</p>
				<p>• Staff should be at <strong>north</strong> (start position)</p>
			</div>
		</div>
		
		<div class="expected-result">
			<h3>Expected Result</h3>
			<p>✅ Blue arrow at <strong>southwest</strong> corner (not south)</p>
			<p>✅ Red arrow at <strong>northeast</strong> corner (not north)</p>
			<p>✅ Blue staff at south position</p>
			<p>✅ Red staff at north position</p>
			<p>✅ Letter A at bottom left</p>
		</div>
	</div>
</main>

<style>
	main {
		padding: 2rem;
		text-align: center;
		font-family: system-ui, sans-serif;
		max-width: 1000px;
		margin: 0 auto;
	}

	.pictograph-container {
		margin: 2rem 0;
		border: 2px solid #333;
		display: inline-block;
		padding: 1rem;
		background: white;
		border-radius: 8px;
		box-shadow: 0 4px 8px rgba(0,0,0,0.1);
	}

	.explanation {
		text-align: left;
		margin-top: 2rem;
		background: #f8f9fa;
		padding: 2rem;
		border-radius: 8px;
		border: 1px solid #dee2e6;
	}

	.explanation h2 {
		margin-top: 0;
		color: #333;
	}

	code {
		background: #e9ecef;
		padding: 0.25rem 0.5rem;
		border-radius: 4px;
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
	}

	.location-calcs {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		margin: 1.5rem 0;
	}

	.calc {
		border: 1px solid #ddd;
		padding: 1rem;
		border-radius: 6px;
		background: white;
	}

	.blue-calc {
		border-left: 4px solid #2E3192;
	}

	.red-calc {
		border-left: 4px solid #ED1C24;
	}

	.calc h3 {
		margin: 0 0 1rem 0;
		font-size: 1.1rem;
	}

	.calc p {
		margin: 0.5rem 0;
		font-size: 0.9rem;
	}

	.expected-result {
		background: #d4edda;
		border: 1px solid #c3e6cb;
		border-radius: 6px;
		padding: 1rem;
		margin-top: 1.5rem;
	}

	.expected-result h3 {
		margin-top: 0;
		color: #155724;
	}

	.expected-result p {
		margin: 0.5rem 0;
		color: #155724;
		font-weight: 500;
	}

	h1 {
		color: #333;
		margin-bottom: 0.5rem;
	}

	strong {
		color: #007bff;
	}
</style>
