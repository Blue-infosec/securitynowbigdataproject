<div ng-controller="dataController" ng-model="thedata">
    Search For anything in all the episodes: <input type="text" id="search" ng-model="searchval"/><br/><br/>
    <article data-ng-repeat="data in thedata">
        <secnow chez="data"></secnow>
    </article>
</div>