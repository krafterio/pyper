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

        // Register services
        serviceRegistry.add("command", {
            openMainPalette: () => {},
            start: () => {},
        });
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