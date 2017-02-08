let Details = function() {

  this.render = function(data) {
    this.reset();

    $("#current-step").html(data.step)

    const detailsTag = `<div class="details-content"></div>`;
    const details = $(detailsTag)[0];
    $(".details").append(details)

    if (data) {
      if (data.type === "BaseStation") {
        this.renderBaseStation(data);
      } else if (data.type === "UAV") {
        this.renderUav(data);
      } else if (data.type === "Item") {
        this.renderItem(data);
      }
    }

  }

  this.renderBaseStation = function(data) {
    const colors = {
      1: "bg-success",
      2: "bg-warning",
      3: "bg-danger",
      4: "bg-info"
    }

    const header = $(`<h4>BaseStation ${data.id}</h4>`)[0];
    const position = $(this.renderRow("Position", `${data.x}, ${data.y}, ${data.z}`))[0];
    const totalItems = $(this.renderRow("Total Items", data.total_items))[0];
    const pickedUpItems = $(this.renderRow("Picked up Items", data.picked_up_item))[0];
    const waitingItems = $(this.renderRow("Waiting Items", data.waiting_items))[0];

    const itemStatus = $(`<p>Waiting items by priority:</p>`)[0];
    let itemProgressString = `<div class="progress">`;
    for (let priority in data.waiting_items_by_priority) {
      if (data.waiting_items_by_priority.hasOwnProperty(priority)) {
        let percentage = data.waiting_items_by_priority[priority] / data.max_items * 100;
        itemProgressString += `<div class="progress-bar ${colors[priority]}" role="progressbar" style="width: ${percentage}%" aria-valuenow="${data.waiting_items_by_priority[priority]}" aria-valuemin="0" aria-valuemax="${data.max_items}">${priority}</div>`;
      }
    }
    itemProgressString += `</div>`;

    const itemProgress = $(itemProgressString)[0];

    $(".details-content").append(header);
    $(".details-content").append(position);
    $(".details-content").append(totalItems);
    $(".details-content").append(pickedUpItems);
    $(".details-content").append(waitingItems);
    $(".details-content").append(itemStatus);
    $(".details-content").append(itemProgress);
  }

  this.renderUav = function(data) {
    const header = $(`<h4>UAV ${data.id}</h4>`)[0];
    const position = $(this.renderRow("Position", `${data.x}, ${data.y}, ${data.z}`))[0];
    const destination = $(this.renderRow("Destination", `${data.destination[0]}, ${data.destination[1]}, ${data.destination[2]}`))[0];
    let itemLocation = "";
    if (data.item) {
      itemLocation = $(this.renderRow("Item location", `${data.item[0]}, ${data.item[1]}, ${data.item[2]}`))[0];
    }
    const currentChargePercentage = (data.battery_charge / data.battery_max * 100).toFixed(1);
    const isLow = data.battery_low;
    const isEmpty = data.battery_empty;
    let progessColor = "bg-success";
    if (isLow) {
      progessColor = "bg-warning"
    }
    if (isEmpty) {
      progessColor = "bg-danger"
    }

    const batteryStatus = $(`<p>Battery status:</p>`)[0];
    const batteryProgress = $(`<div class="progress">
      <div class="progress-bar ${progessColor} progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="${currentChargePercentage}" aria-valuemin="0" aria-valuemax="100" style="width: ${currentChargePercentage}%">${currentChargePercentage}%</div>
    </div>`)[0];


    $(".details-content").append(header);
    $(".details-content").append(position);
    $(".details-content").append(destination);
    if (data.item) {
      $(".details-content").append(itemLocation);
    }
    $(".details-content").append(batteryStatus);
    $(".details-content").append(batteryProgress);
  }

  this.renderItem = function(data) {
    const header = $(`<h4>Item ${data.id}</h4>`)[0];
    const position = $(this.renderRow("Position", `${data.x}, ${data.y}, ${data.z}`))[0];
    const priority = $(this.renderRow("Priority", data.priority))[0];
    const lifetime = $(this.renderRow("Lifetime", data.lifetime))[0];

    $(".details-content").append(header);
    $(".details-content").append(position);
    $(".details-content").append(priority);
    $(".details-content").append(lifetime);
  }

  this.renderRow = function(key, value) {
    return `<div class="row"><div class="col-7">${key}:</div><div class="col">${value}</div></div>`
  }

  this.reset = function() {
    $(".details").empty();
  }
}
