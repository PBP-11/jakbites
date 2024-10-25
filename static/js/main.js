//buat att main

async function filter(){
    const searchInput = document.getElementById("inputanQuery").value;
    const kotak = document.getElementById("searchBox");
    const restoList = document.getElementById("restoList");
    const foodList = document.getElementById("foodList");
    const tagErr = document.getElementById("notfound")
    const garis = document.getElementById("garisPemisah")

    const filterSelect = document.getElementById('filterSelect').value;
    console.log(filterSelect);

    if(filterSelect === "Restaurant Only"){
        restoList.classList.remove("hidden")
        foodList.classList.add("hidden")
        garis.classList.add("hidden")
    }else if(filterSelect === "Food Only"){
        foodList.classList.remove("hidden")
        restoList.classList.add("hidden")
        garis.classList.add("hidden")
    }else if(filterSelect === "Search All"){
        foodList.classList.remove("hidden")
        restoList.classList.remove("hidden")
        garis.classList.remove("hidden")
    }
}

async function search() {
    const searchInput = document.getElementById("inputanQuery").value;
    const kotak = document.getElementById("searchBox");
    const restoList = document.getElementById("restoList");
    const foodList = document.getElementById("foodList");
    const tagErr = document.getElementById("notfound")
    const garis = document.getElementById("garisPemisah")

    //buat hide unhide aja
    try {
        const response = await fetch(`/search?query=${searchInput}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            const err = await response.json();
            console.log(err.message);
            return;
        }

        const result = await response.json();
        console.log(result);

        // Show the search box only if input is more than 2 characters
        if (searchInput.length > 2) {
            kotak.classList.remove("hidden");
            garis.classList.remove("hidden")

            if (result.length === 0) {
                tagErr.classList.remove("hidden")
                tagErr.innerHTML = "No results found"
                restoList.classList.add("hidden")
                foodList.classList.add("hidden")
                kotak.classList.add("w-[40%]")
                kotak.classList.remove("w-auto")
            } else {
                kotak.classList.add("w-auto")
                kotak.classList.remove("w-[40%]")
                tagErr.classList.add("hidden")
                restoList.classList.remove("hidden")
                foodList.classList.remove("hidden")

                const uniqueRestaurants = new Map(
                    result
                        .filter(item => item.restaurant) 
                        .map(item => [item.restaurant.restaurant_name, item.restaurant.location])  // Get unique name-location pairs
                );

                restoList.innerHTML = Array.from(uniqueRestaurants.entries())
                    .map(([name, location]) => `
                        <div class="flex items-center gap-2">
                            <svg class = "w-5 h-5" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path class = "fill-white" d="M13.925 5.15001V4.85001C13.925 4.75001 13.9 4.65001 13.85 4.57501L11.95 1.22501C11.675 0.750012 11.175 0.450012 10.625 0.450012H3.37501C2.82501 0.450012 2.32501 0.750012 2.05001 1.22501L0.150012 4.57501V4.60001C0.150012 4.62501 0.125012 4.65001 0.125012 4.67501C0.100012 4.72501 0.0750122 4.80001 0.0750122 4.87501V14.075C0.0750122 14.925 0.750012 15.6 1.60001 15.6H12.375C13.225 15.6 13.9 14.925 13.9 14.075L13.925 5.15001ZM6.40001 5.40001C6.30001 5.85001 5.87501 6.17501 5.40001 6.17501C4.92501 6.17501 4.52501 5.85001 4.40001 5.40001H6.40001ZM3.02501 1.77501C3.10001 1.65001 3.22501 1.57501 3.37501 1.57501H10.625C10.775 1.57501 10.9 1.65001 10.975 1.77501L12.375 4.27501H1.62501L3.02501 1.77501ZM12.75 5.40001C12.65 5.85001 12.25 6.17501 11.75 6.17501C11.275 6.17501 10.875 5.85001 10.75 5.40001H12.75ZM9.57501 5.40001C9.47501 5.85001 9.07501 6.17501 8.57501 6.17501C8.07501 6.17501 7.70001 5.85001 7.57501 5.40001H9.57501ZM3.22501 5.40001C3.12501 5.85001 2.72501 6.17501 2.22501 6.17501C1.75001 6.17501 1.35001 5.85001 1.22501 5.40001H3.22501ZM3.75001 14.45V10.575C3.75001 10.525 3.80001 10.475 3.85001 10.475H5.05001C5.10001 10.475 5.15001 10.525 5.15001 10.575V14.425H3.75001V14.45ZM12.4 14.45H6.30001V10.575C6.30001 9.90001 5.75001 9.35001 5.07501 9.35001H3.87501C3.20001 9.35001 2.65001 9.90001 2.65001 10.575V14.425H1.62501C1.40001 14.425 1.22501 14.25 1.22501 14.025V7.02501C1.52501 7.20001 1.87501 7.27501 2.25001 7.27501C2.87501 7.27501 3.45001 7.00001 3.85001 6.57501C4.25001 7.00001 4.80001 7.27501 5.45001 7.27501C6.07501 7.27501 6.65001 7.00001 7.05001 6.57501C7.45001 7.00001 8.00001 7.27501 8.65001 7.27501C9.27501 7.27501 9.85001 7.00001 10.25 6.57501C10.65 7.00001 11.2 7.27501 11.85 7.27501C12.225 7.27501 12.575 7.17501 12.875 7.02501V14.025C12.8 14.25 12.6 14.45 12.4 14.45Z" fill="black"/>
                            </svg>
                            <div class = "p-2 transition ease-in-out hover:scale-105 hover:text-white hover:bg-gray-500 rounded-xl">
                               //kalo mao ngelink ganti disini wir 
                                <a href = "link">
                                    <p class="text-sm line-clamp-1 font-[Poppins] font-bold">${name}</p>
                                    <p class="text-[10px] font-[Lora] ">${location.charAt(0).toUpperCase() + location.slice(1)}</p>
                                </a>
                            </div>
                        </div>
                    `)
                    .join("");

                foodList.innerHTML = result
                    .filter(item => item.food_name) 
                    .map(item => {
                        return `<div class = "flex items-center gap-2">
                                    <svg class = "h-5 w-5" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path class = "fill-white" d="M15.84 10.6299C16.2405 10.6349 16.638 10.5596 17.009 10.4084C17.38 10.2573 17.7169 10.0334 18 9.74991L20.83 6.91991C21.0162 6.73255 21.1208 6.4791 21.1208 6.21491C21.1208 5.95073 21.0162 5.69728 20.83 5.50991C20.737 5.41618 20.6264 5.34179 20.5046 5.29102C20.3827 5.24025 20.252 5.21411 20.12 5.21411C19.988 5.21411 19.8573 5.24025 19.7354 5.29102C19.6136 5.34179 19.5029 5.41618 19.41 5.50991L16.55 8.32991C16.457 8.42364 16.3464 8.49803 16.2246 8.5488C16.1027 8.59957 15.972 8.62571 15.84 8.62571C15.708 8.62571 15.5773 8.59957 15.4554 8.5488C15.3336 8.49803 15.2229 8.42364 15.13 8.32991L18.67 4.79991C18.7632 4.70667 18.8372 4.59598 18.8876 4.47416C18.9381 4.35234 18.9641 4.22177 18.9641 4.08991C18.9641 3.95805 18.9381 3.82749 18.8876 3.70566C18.8372 3.58384 18.7632 3.47315 18.67 3.37991C18.5767 3.28667 18.4661 3.21271 18.3442 3.16225C18.2224 3.11179 18.0918 3.08582 17.96 3.08582C17.8281 3.08582 17.6976 3.11179 17.5757 3.16225C17.4539 3.21271 17.3432 3.28667 17.25 3.37991L13.72 6.91991C13.5337 6.73255 13.4292 6.4791 13.4292 6.21491C13.4292 5.95073 13.5337 5.69728 13.72 5.50991L16.55 2.67991C16.6432 2.58667 16.7172 2.47598 16.7676 2.35416C16.8181 2.23234 16.8441 2.10177 16.8441 1.96991C16.8441 1.83805 16.8181 1.70748 16.7676 1.58566C16.7172 1.46384 16.6432 1.35315 16.55 1.25991C16.4567 1.16667 16.3461 1.09271 16.2242 1.04225C16.1024 0.991792 15.9718 0.96582 15.84 0.96582C15.7081 0.96582 15.5776 0.991792 15.4557 1.04225C15.3339 1.09271 15.2232 1.16667 15.13 1.25991L12.3 4.08991C11.7382 4.65241 11.4226 5.41491 11.4226 6.20991C11.4226 7.00491 11.7382 7.76741 12.3 8.32991L11 9.61991L2.72999 1.31991L2.62999 1.25991C2.57887 1.21531 2.52162 1.17827 2.45999 1.14991L2.27999 1.07991L2.15999 0.999912H2.08999H1.88999C1.83037 0.990379 1.76961 0.990379 1.70999 0.999912C1.64945 1.02195 1.59224 1.05223 1.53999 1.08991L1.37999 1.18991H1.30999L1.24999 1.28991C1.20766 1.34271 1.17081 1.39967 1.13999 1.45991C1.1107 1.52089 1.08726 1.58451 1.06999 1.64991C1.06999 1.64991 1.06999 1.71991 1.06999 1.75991C0.827323 3.45132 0.982037 5.17601 1.52186 6.79723C2.06169 8.41844 2.97179 9.89161 4.17999 11.0999L6.81999 13.7299L1.40999 19.1299C1.31626 19.2229 1.24186 19.3335 1.1911 19.4553C1.14033 19.5772 1.11419 19.7079 1.11419 19.8399C1.11419 19.9719 1.14033 20.1026 1.1911 20.2245C1.24186 20.3463 1.31626 20.4569 1.40999 20.5499C1.50343 20.6426 1.61424 20.7159 1.73608 20.7657C1.85792 20.8154 1.98838 20.8407 2.11999 20.8399C2.25159 20.8407 2.38206 20.8154 2.50389 20.7657C2.62573 20.7159 2.73655 20.6426 2.82999 20.5499L8.89999 14.5699L11.73 11.7399L13.73 9.73991C14.288 10.3039 15.0466 10.6239 15.84 10.6299ZM8.18999 12.4499L5.55999 9.80991C4.11844 8.34865 3.21583 6.44118 2.99999 4.39991L9.60999 10.9999L8.18999 12.4499ZM14.43 13.0199C14.2417 12.8303 13.9858 12.7232 13.7185 12.7223C13.4513 12.7213 13.1946 12.8266 13.005 13.0149C12.8154 13.2032 12.7083 13.4591 12.7074 13.7264C12.7064 13.9936 12.8117 14.2503 13 14.4399L19.3 20.7399C19.491 20.9137 19.7418 21.0069 20 20.9999C20.1316 21.0007 20.2621 20.9754 20.3839 20.9257C20.5057 20.8759 20.6165 20.8026 20.71 20.7099C20.8037 20.6169 20.8781 20.5063 20.9289 20.3845C20.9796 20.2626 21.0058 20.1319 21.0058 19.9999C21.0058 19.8679 20.9796 19.7372 20.9289 19.6153C20.8781 19.4935 20.8037 19.3829 20.71 19.2899L14.43 13.0199Z" fill="black"/>
                                    </svg>
                                <div class = "p-2 transition ease-in-out hover:scale-105 hover:text-white hover:bg-gray-500 rounded-xl">
                                    /kalo mao ngelink ganti disini wir 
                                    <a href = "link">
                                        <p class = " text-sm line-clamp-1 font-[Poppins] font-bold">
                                        ${item.food_name.split(" ").slice(0,5).join(" ")}
                                        </p>
                                        <p class = "text-[10px] font-[Lora]">
                                            ${item.restaurant.restaurant_name}
                                        </p>
                                    </a>
                                </div>
                            </div>`
                    })
                    .join("");
            }
            //reset all
        } else {
            kotak.classList.add("hidden");
        }
    } catch (error) {
        console.log(error);
    }
}
