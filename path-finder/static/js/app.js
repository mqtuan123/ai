let map;
let routeLine;

const startSelect =
document.getElementById("startNode");

const endSelect =
document.getElementById("endNode");

const findBtn =
document.getElementById("findBtn");


function initMap(){

    map = L.map("map").setView(
        [21.005, 105.845],
        16
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                "© OpenStreetMap"
        }
    ).addTo(map);
}


async function loadNodes(){

    const response =
        await fetch("/api/nodes");

    const nodes =
        await response.json();

    nodes.forEach(node => {

        let option1 =
            document.createElement("option");

        option1.value = node.id;
        option1.text =
            `Node ${node.id}`;

        startSelect.appendChild(option1);

        let option2 =
            document.createElement("option");

        option2.value = node.id;
        option2.text =
            `Node ${node.id}`;

        endSelect.appendChild(option2);

        L.circleMarker(
            [
                node.lat,
                node.lng
            ],
            {
                radius: 3
            }
        ).addTo(map);

    });

}


async function findPath(){

    const start =
        startSelect.value;

    const end =
        endSelect.value;

    const response =
        await fetch(
            "/api/find-path",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    start,
                    end
                })
            }
        );

    const result =
        await response.json();

    const coords =
        result.path.map(
            p => [p.lat, p.lng]
        );

    if(routeLine){
        map.removeLayer(routeLine);
    }

    routeLine =
        L.polyline(
            coords,
            {
                color: "red",
                weight: 6
            }
        ).addTo(map);

    map.fitBounds(
        routeLine.getBounds()
    );
}


findBtn.addEventListener(
    "click",
    findPath
);

initMap();
loadNodes();