interface Device {
	codename: string | string[];
	deviceName: string;
	brandName: string;
	otaEnabled: boolean;
	latestVersion: string;
	discontinued: boolean;
	deviceChangelog: Changelog[] | null;
	releases: Releases[] | null;
	maintainerInfo: Maintainer;
	links: Links;
}
interface Changelog {
	timestamp: number;
	changes: string[] | string;
}
interface Releases {
	type: "gapps" | "vanilla";
	generatedAt: number;
	hash: string;
	fileName: string;
	url: string;
	requireCleanFlash: boolean;
	images: Images[] | null;
	size: number;
	version: string;
	latest: boolean;
}
interface Images {
	type: "boot" | "recovery";
	url: string;
}
interface Maintainer {
	name: string | null;
	profileURL: string | null;
}
interface Links {
	xda: string | null;
	telegram: string | null;
}
