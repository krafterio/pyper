/** @odoo-module **/

import { registry } from "@web/core/registry";
import { makeTestEnv } from "@web/../tests/helpers/mock_env";
import { getFixture, mount } from "@web/../tests/helpers/utils";
import { SearchMenu } from '@pyper_command_search/core/web/search_menu';

const serviceRegistry = registry.category("services");
const systrayRegistry = registry.category("systray");

let target;

QUnit.module("PyperCommandSearch", {
    async beforeEach() {
        // Prepare the test target
        target = getFixture();

        // Register the SearchMenu component in the systray
        systrayRegistry.add("pyper_command_search.search_menu", { Component: SearchMenu });

        // Mock command service
        const commandServiceMock = {
            openMainPalette() {
                commandServiceMock.commandPaletteOpened = true;
            },
            start: () => {},
            commandPaletteOpened: false,
        };
        
        // Register the mocked service
        serviceRegistry.add("command", commandServiceMock);
    },
});

QUnit.test("TestSearchSystrayExists", async (assert) => {
    const env = await makeTestEnv({});
    await mount(SearchMenu, target, { env });

    const searchMenuElement = target.querySelector(".o-command-search-SearchSystray-class");
    assert.ok(
        searchMenuElement,
        "Search Menu is rendered with the class .o-command-search-SearchSystray-class"
    );
});

QUnit.test("TestOpenSystray", async (assert) => {
    let env = await makeTestEnv({});

    const commandService = serviceRegistry.get("command");
    // Pass the mocked command service to the searchMenu
    env.services.command = commandService;

    await mount(SearchMenu, target, { env });

    const button = target.querySelector(".dropdown-toggle");
    commandService.commandPaletteOpened = false;

    button.click();
    assert.ok(
        commandService.commandPaletteOpened,
        "Command palette should open when the button is clicked"
    );
});
